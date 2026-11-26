# DovSG

- Catalog ordinal: 194 ([project catalog](../data/memory-systems.json))
- Listed repository: [BJHYZJ/DovSG](https://github.com/BJHYZJ/DovSG)
- Default branch: `master`
- Reviewed revision: [`b355987a1ca586f7756f025820fddc24166d75af`](https://github.com/BJHYZJ/DovSG/commit/b355987a1ca586f7756f025820fddc24166d75af)
- Review timestamp: 2026-11-25 11:20:57 UTC (2026-11-25 03:20:57 PST; America/Los_Angeles)
- Review status: **Reviewed from code**
- Benchmark status: **Benchmark not run**

GitHub identifies `master` as the default branch; its official branch feed reports the full head SHA above, last updated 2025-04-17T10:23:08Z. ([repository](https://github.com/BJHYZJ/DovSG), [branches](https://github.com/BJHYZJ/DovSG/branches), [master history](https://github.com/BJHYZJ/DovSG/commits/master.atom), [head commit](https://github.com/BJHYZJ/DovSG/commit/b355987a1ca586f7756f025820fddc24166d75af))

## Summary

DovSG is a research system for mobile manipulation that builds and locally updates a 3D scene graph from RGB-D observations. Its object memory combines voxelized geometry with image and text features; an LLM planner decomposes task instructions while localization and robot modules carry out the subtasks. The observations here describe inspected source and documentation, not measured memory quality or operational performance.

## Who and what

The official README presents DovSG as the implementation accompanying a 2025 robotics paper on dynamic open-vocabulary 3D scene graphs for long-term language-guided mobile manipulation. It is a research codebase integrating perception, mapping, planning, navigation, and manipulation rather than a standalone memory service. The README describes an xArm6 on an Agilex mobile base with a RealSense D455 camera and provides a demo workflow. The pinned Atlas roster record is retained only for catalog identity and locator attribution, not as assessment evidence. ([roster attribution](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dovsg.md)) ([README](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/README.md))

## Architecture and data model

The documented pipeline collects RGB-D frames, estimates camera poses with DROID-SLAM, aligns the scene, trains ACE for relocalization, and constructs a view dataset. RAM image tagging supplies open-vocabulary prompts; GroundingDINO and SAM2 produce object masks; CLIP encodes image crops and text labels. The controller connects this scene-memory path to task planning, localization, navigation, and the robot interface. ([README](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/README.md), [semantic memory](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/ram_groundingdino_sam2_clip_semantic_memory.py), [controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py))

An instance record carries a class name and generated class ID, confidence, detection count, mask and image references, a 3D voxel-index set, bounding box, and CLIP image/text features. The instance processor associates detections with existing objects using weighted spatial, visual, and text similarity; the inspected defaults are 0.5, 0.4, and 0.1, with a 0.75 merge threshold. ([instance processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/instances/instance_process.py))

A scene graph contains object nodes with parent/child links, class and ID, parent relation, and a part marker. The graph processor derives parent relations from geometry (the inspected code includes an `inside` relation); the graph implementation also supports visualization. The controller stores each step’s view dataset, instance list, scene graph, and LightGlue features as local serialized artifacts under a directory keyed by scene tag, configuration suffix, and step number. ([graph model](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/graph.py), [scene-graph processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/scene_graph_processer.py), [controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py))

## Write, update, delete, and retrieval

**Write.** Semantic processing tags each frame, detects and segments prompted objects, computes CLIP features, and associates observations into instance objects. Geometry is represented through points/voxel indexes derived from the view dataset. The scene graph is then built from the instance set and geometric relations. ([semantic memory](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/ram_groundingdino_sam2_clip_semantic_memory.py), [instance processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/instances/instance_process.py), [scene-graph processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/scene_graph_processer.py))

**Update and removal.** After an interaction, the controller advances the step, computes indexes to remove from new observations, updates the view dataset and LightGlue features, updates instances, rebuilds/updates the scene graph against the previous graph, and saves the resulting step. The graph update code removes nodes whose IDs are absent from the new instance set and handles affected descendants before rebuilding. This is current-state repair; the inspected path does not expose a separate mutation ledger explaining each removed object. ([controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py), [scene-graph processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/scene_graph_processer.py), [graph model](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/graph.py))

**Retrieval.** The inspected localizer embeds a text query with CLIP and ranks stored instance features. A single-object query returns the centroid of the highest-scoring instance. For a relation-like “A on B” request, it takes the top three candidates for A and top five for B, then returns the A candidate nearest any B candidate. In this inspected method the scene graph is not traversed to answer that query; it performs feature ranking and centroid selection. ([instance localizer](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/navigation/instances_localizer.py))

The task planner sends a description to GPT-4o-mini with fixed examples and saves its response as JSON for reuse. The inspected planner call does not pass the scene graph as prompt context. The README describes the graph as part of the perception/action pipeline, but how graph facts influence every planning decision was not established by the selected files. ([task planner](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/task_planning/gpt_task_planning.py), [README](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/README.md))

## Scope isolation

The local storage path includes a caller-supplied scene tag and parameter suffix, with numbered step directories. The inspected code shows no user/tenant authorization layer or enforced boundary separating scene tags; isolation therefore appears to rely on local path/configuration discipline. Cross-process or multi-user isolation was not assessed. ([controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py))

## Provenance and evidence

Object state retains image names, mask indexes, detector confidence, detection counts, class identity, and visual/text embeddings, while each step stores serialized snapshots. These fields can connect an object to observations, but the selected implementation does not establish a claim-level source/evidence model, trust state, or append-only mutation audit. The persisted step history may permit comparison across snapshots; its completeness and recovery behavior were not exercised. ([instance processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/instances/instance_process.py), [controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py))

## Efficiency and observability

The visible implementation uses substantial perception components (RAM, GroundingDINO, SAM2, CLIP, point-cloud/voxel processing, and feature matching). Instance processing exposes similarity thresholds and periodic denoising; controller debug/progress output and saved point-cloud/graph artifacts are inspection surfaces. It saves the full view dataset, objects, graph, and LightGlue features for each step, so storage growth and update latency depend on scene size and interaction history. The reviewed material provides no measured latency, token, cost, or storage results and no service-style telemetry dashboard. ([semantic memory](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/ram_groundingdino_sam2_clip_semantic_memory.py), [instance processing](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/instances/instance_process.py), [controller](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py))

## Metric-domain evidence

All entries below are **code observations**, not measured outcomes. No DovSG benchmark or runtime was run.

| Metric domain | Evidence status |
|---|---|
| Answerable retrieval accuracy | Unmeasured. CLIP similarity and candidate selection are implemented; no retrieval cases were scored. |
| Abstention | Unknown/unmeasured. The inspected localizer selects a top match; no evaluated answerability threshold or abstention quality was established. |
| Correction accuracy and stale-value rate | Unmeasured. New observations update object and graph state; no correction workload was run. |
| Deletion leakage | Unmeasured. Source shows scene-graph node removal when objects disappear from the updated set; no post-deletion retrieval checks were run. |
| Scope isolation leakage | Unmeasured. Scene-tag paths are visible, but cross-scope enforcement was not established. |
| Evidence support and citation coverage | Unmeasured. Object observations retain detection metadata; no evidence-grounded answer workload exists in the inspected path. |
| Retrieval latency | Unmeasured. No timing sample was collected. |
| Write-to-recall delay | Unmeasured. No write/retrieval timing or success measurement was collected. |
| Tokens and cost | Unmeasured. The task planner uses an OpenAI model in code, but no token or price observations were collected. |
| Storage efficiency | Unmeasured. Per-step serialized artifacts are visible; no storage-size sample or retention experiment was performed. |

Metric definitions are in [METRICS.md](../METRICS.md); benchmark execution status is tracked in [initial-baselines-status.json](../results/initial-baselines-status.json). The workload fixture at [memory-benchmark-v1.json](../fixtures/memory-benchmark-v1.json) was not executed.

## Limits and unknowns

This review inspected the official README and selected memory, instance, graph, controller, localization, and planning source files at one verified head. It did not inspect every robotics, hardware, navigation, manipulation, evaluation, or dependency path. No DovSG runtime, tests, or benchmarks were run. The docs describe a specific Ubuntu/ROS/GPU/robot environment; hardware availability, reproducibility, recovery after partial writes, large-scene scaling, and the reliability of object identity/relocalization remain unverified here. The selected localizer ranks by text/image similarity and returns centroids; its behavior under ambiguous labels, absent objects, or changing scenes was not measured.

## Contact

The official pinned README was checked for a published contact email; none was found. No commit/profile metadata or third-party directory was used.

## Sources

- [Official repository](https://github.com/BJHYZJ/DovSG)
- [Default branch metadata](https://github.com/BJHYZJ/DovSG/branches)
- [Official master history feed](https://github.com/BJHYZJ/DovSG/commits/master.atom)
- [Reviewed head commit](https://github.com/BJHYZJ/DovSG/commit/b355987a1ca586f7756f025820fddc24166d75af)
- [Official README at reviewed SHA](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/README.md)
- [Semantic perception and feature extraction](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/ram_groundingdino_sam2_clip_semantic_memory.py)
- [Instance association and object records](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/instances/instance_process.py)
- [Scene graph relations and update](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/scene_graph_processer.py)
- [Scene graph data model](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/memory/scene_graph/graph.py)
- [Controller and per-step persistence](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/controller.py)
- [CLIP instance localizer](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/navigation/instances_localizer.py)
- [LLM task planner](https://github.com/BJHYZJ/DovSG/blob/b355987a1ca586f7756f025820fddc24166d75af/dovsg/task_planning/gpt_task_planning.py)
- [Project metric definitions](../METRICS.md)
- [Project benchmark fixture](../fixtures/memory-benchmark-v1.json)
- [Project benchmark execution status](../results/initial-baselines-status.json)
- [Curated roster attribution (identity and locator only)](https://github.com/neoneye/agent-memory-atlas/blob/19199a4fc249e89c0793be06f0b166b358089ba0/content/systems/dovsg.md)
