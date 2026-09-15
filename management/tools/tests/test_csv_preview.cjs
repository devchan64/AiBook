// Run: node --test management/tools/tests/test_csv_preview.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const script = fs.readFileSync(path.resolve(__dirname, '../../../docs/javascripts/csv-preview.js'), 'utf8');
class Element {
  constructor(tag) { this.tagName = tag; this.children = []; this.dataset = {}; this.attrs = {}; this.listeners = {}; }
  appendChild(child) { this.children.push(child); return child; }
  setAttribute(key, value) { this.attrs[key] = value; }
  getAttribute(key) { return this.attrs[key]; }
  addEventListener(key, fn) { this.listeners[key] = fn; }
  insertAdjacentElement(_, node) { this.next = node; }
  replaceChild(next, old) { const i = this.children.indexOf(old); assert.notEqual(i, -1); this.children[i] = next; }
  click() { return this.listeners.click(); }
}
function setup(hrefs, fetch) {
  const links = hrefs.map(href => Object.assign(new Element('a'), { href, attrs: {href} }));
  const document = { baseURI: 'https://example.test/book/', readyState: 'complete',
    createElement: tag => new Element(tag), querySelectorAll: () => links };
  let init;
  vm.runInNewContext(script, { document, URL, fetch, document$: {subscribe(fn) { init = fn; fn(); }} });
  return { links, init };
}
function find(node, tag) { return [ ...(node.tagName === tag ? [node] : []), ...node.children.flatMap(c => find(c, tag)) ]; }
const response = text => ({ok:true, text:async () => text});
test('CSV query/hash/uppercase paths initialize once; non-CSV is ignored', () => {
  const {links, init} = setup(['https://example.test/A.CSV?v=2#top', 'https://example.test/a.json'], () => {});
  const button = links[0].next; assert.ok(button); assert.equal(links[1].next, undefined);
  init(); assert.equal(links[0].next, button); assert.equal(button.attrs['aria-controls'], button.next.id);
});
test('rapid close and reopen shares the in-flight fetch and caches result', async () => {
  let calls = 0, resolve;
  const {links} = setup(['https://example.test/a.csv'], () => {calls++; return new Promise(r => resolve=r);});
  const button = links[0].next, panel = button.next;
  const first = button.click(); await button.click(); await button.click(); assert.equal(calls,1);
  resolve(response('\uFEFFname,value\r\n"a,b","say ""hi"""\r\n"two\nlines",2\r\n'));
  await first; assert.equal(panel.hidden, false); assert.equal(panel.attrs['aria-busy'],'false');
  const cells = find(panel,'td').map(c => c.textContent);
  assert.deepEqual(cells, ['a,b','say "hi"','two\nlines','2']);
  assert.equal(find(panel,'th')[0].textContent,'name');
  await button.click(); await button.click(); assert.equal(calls,1);
});
test('failed requests can be retried and row previews are limited to 12', async () => {
  let calls=0;
  const {links}=setup(['https://example.test/a.csv'], async () => ++calls===1 ? {ok:false,status:404} : response('n\n'+Array.from({length:20},(_,i)=>i).join('\n')));
  const button=links[0].next, panel=button.next; await button.click();
  assert.match(panel.children[0].textContent,/404/); await button.click(); await button.click();
  assert.equal(calls,2); assert.equal(find(panel,'td').length,12);
});
test('empty input renders a readable empty state',async()=>{
  const {links}=setup(['https://example.test/empty.csv'],async()=>response(''));
  const button=links[0].next; await button.click(); assert.match(button.next.children[0].textContent,/행이 없습니다/);
});
