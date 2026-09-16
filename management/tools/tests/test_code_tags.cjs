const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const script = fs.readFileSync(path.resolve(__dirname,'../../../docs/javascripts/code-tags.js'),'utf8');
function block(tag, classes='', parentHighlight=false, excluded=false) {
  return {tagName:tag,className:classes,dataset:{},tags:[],
    closest: selector=>selector==='.highlight'?parentHighlight:excluded,
    querySelector: ()=>({className:''}),
    insertBefore(tag){this.tags.push(tag);},
    insertAdjacentElement(where,tag){assert.equal(where,'beforebegin');this.tags.push(tag);}};
}
function run(blocks) {
  let init;
  vm.runInNewContext(script,{document:{querySelectorAll:selector=>selector === ".aibook-code-language + .mermaid" ? [] : blocks,createElement:()=>({})},
    document$:{subscribe(fn){init=fn;fn();}}});
  return init;
}
test('labels fenced languages and plain code once without tagging line-number pre elements',()=>{
  const python=block('DIV','language-python highlight');
  const plain=block('PRE');
  const gutter=block('PRE','',true);
  const json=block('DIV','language-json highlight');
  const init=run([python,plain,gutter,json]); init();
  assert.deepEqual(python.tags.map(t=>t.textContent),['Python']);
  assert.deepEqual(plain.tags.map(t=>t.textContent),['Text']);
  assert.deepEqual(json.tags.map(t=>t.textContent),['JSON']);
  assert.equal(gutter.tags.length,0);
});
test('does not duplicate preview tags or tag rendered diagrams',()=>{
  const preview=block('PRE','language-python',false,true);
  const diagram=block('PRE','mermaid',false,true);
  run([preview,diagram]);
  assert.equal(preview.tags.length,0);assert.equal(diagram.tags.length,0);
});

test('removes the temporary Text tag when Material replaces its pending source with a diagram',()=>{
  let callback, removed=0;
  const diagram={previousElementSibling:{remove(){removed++;}}};
  vm.runInNewContext(script,{
    document:{documentElement:{},querySelectorAll:selector=>selector === ".aibook-code-language + .mermaid" ? [diagram] : []},
    MutationObserver:class {constructor(fn){callback=fn;}observe(){}},
    document$:{subscribe(){}},
  });
  callback(); assert.equal(removed,1);
});
