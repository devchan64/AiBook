"""ANNY NPZ를 Blender 4.5.3 메시·리그와 정적 GLB로 저장한다. bpy 전용 Python에서 실행."""
import argparse
import json
from pathlib import Path
import bpy
import numpy as np
from mathutils import Matrix, Vector


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--height', type=float, default=1.6)
    args = parser.parse_args()
    if bpy.app.version[:3] != (4, 5, 3):
        raise RuntimeError('bpy 4.5.3 필요')
    if not np.isfinite(args.height) or args.height <= 0:
        raise ValueError('잘못된 목표 높이')
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in ['body.blend', 'body.glb', 'validation.json']:
        if (out / name).exists():
            raise FileExistsError(out / name)
    with np.load(args.bundle, allow_pickle=False) as bundle:
        vertices = bundle['vertices'].copy()
        faces = bundle['faces'].copy()
        matrices = bundle['bone_matrices'].copy()
        names = bundle['bone_names'].tolist()
        parents = bundle['bone_parents'].copy()
        weights, indices = bundle['weights'].copy(), bundle['indices'].copy()
    if not all(np.isfinite(x).all() for x in [vertices, matrices, weights]):
        raise ValueError('비유한 리그 값')
    floor, height = vertices[:, 2].min(), np.ptp(vertices[:, 2])
    if height <= 0:
        raise ValueError('신체 높이 오류')
    scale = args.height / height
    vertices[:, 2] -= floor
    vertices *= scale
    matrices[:, 2, 3] -= floor
    matrices[:, :3, 3] *= scale
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mesh = bpy.data.meshes.new('BodySurface')
    mesh.from_pydata(vertices.tolist(), [], faces.tolist())
    mesh.update()
    body = bpy.data.objects.new('Body', mesh)
    bpy.context.collection.objects.link(body)
    for polygon in mesh.polygons:
        polygon.use_smooth = True
    armature = bpy.data.armatures.new('AnnySkeleton')
    rig = bpy.data.objects.new('Rig', armature)
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    rig.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    # 본 생성과 부모 연결을 분리해 입력 배열 순서에 의존하지 않는다.
    for i, name in enumerate(names):
        bone = armature.edit_bones.new(name)
        bone.head = matrices[i, :3, 3]
        bone.tail = bone.head + Vector((0, .05, 0))
        bone.matrix = Matrix(matrices[i].tolist())
        children = np.where(parents == i)[0]
        if len(children):
            bone.length = max(.015, float(np.linalg.norm(matrices[children[0], :3, 3] - matrices[i, :3, 3])))
    for i, parent in enumerate(parents):
        if parent >= 0:
            armature.edit_bones[names[i]].parent = armature.edit_bones[names[parent]]
    bpy.ops.object.mode_set(mode='OBJECT')
    for name in names:
        body.vertex_groups.new(name=name)
    for vertex, (bone_ids, values) in enumerate(zip(indices, weights)):
        for bone_id, weight in zip(bone_ids, values):
            if weight > 0:
                body.vertex_groups[int(bone_id)].add([vertex], float(weight), 'REPLACE')
    modifier = body.modifiers.new('Skinning', 'ARMATURE')
    modifier.object = rig
    body.parent = rig
    scene = bpy.context.scene
    scene.frame_start = scene.frame_end = 1
    scene.frame_set(1)
    bpy.context.view_layer.update()
    evaluated = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    error = float(np.abs(np.array([v.co[:] for v in evaluated.data.vertices]) - vertices).max())
    weight_error = float(np.abs(weights.sum(1) - 1).max())
    if error > 1e-5 or weight_error > 1e-5:
        raise ValueError(f'리그 검증 실패: rest={error}, weights={weight_error}')
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    rig.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out / 'body.glb'), use_selection=True,
                              export_animations=False, export_all_influences=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'body.blend'))
    (out / 'validation.json').write_text(json.dumps(dict(status='passed', rest_max_error=error,
        weight_sum_max_error=weight_error, bones=len(names), vertices=len(vertices), triangles=len(faces),
        height=args.height, animation_clips=0), indent=2) + '\n')


if __name__ == '__main__':
    main()
