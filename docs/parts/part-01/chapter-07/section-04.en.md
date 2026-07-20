# P1-7.4 Supplemental Learning: From Route Finding to Autonomous-Driving Path Planning

> Section ID: `P1-7.4`
> Version: `v2026.07.20`

Section 7.1 abstracted search as the problem of finding a path to a goal. Section 7.2 explained what heuristics reduce when we cannot inspect every candidate. Section 7.3 separated heuristics from probabilistic models.

This section now shows, through one concrete domain example, how those general ideas are layered inside a real system.

The key question here is:

> how did the route-finding problem become divided into several layers of planning in real systems such as autonomous driving?

The goal is not to explain autonomous-driving technology as a whole. The goal is to use it as a case for understanding how systems represent routes, reduce candidates, and decide immediate actions.

This supplemental section is not the place where the core terms are defined for the first time. `Search`, `search space`, and `computational limit` were introduced in 7.1. `Heuristic` was introduced in 7.2. The boundary between heuristics and probabilistic models was introduced in 7.3. Here we only connect those concepts to a layered real-system example.

Rather than unfolding autonomous-driving technology as a whole, this section focuses on how the route-finding problem splits into `the layer that decides a large route` and `the layer that decides the short trajectory to move right now`. Reinforcement learning itself returns in `P1-8.3` and Part 4 Chapter 19. Here we keep the standard for reading path and trajectory separately.

This section covers only the following:

> the problem of finding a large route  
> and the problem of choosing a short movement to execute right now  
> are usually too different to handle well at the same layer

Then we look at why this difference leads to distinctions such as `global` and `local`, or `path` and `trajectory`.

## Extending Route Finding into Path Planning

- Explain route finding as a bridge between graph search and real driving planning.
- Understand a `waypoint` as a representation of reference points that should be passed.
- Explain at an introductory level the difference between a `global planner` and a `local planner`.
- Avoid using `path` and `trajectory` as if they were the same.
- Read the autonomous-driving case as an extension of more general search and heuristic problems.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| finding a large route and deciding the immediate motion are different problems | This separates abstract route finding from actual vehicle control. | Understand that the big route to the destination and the next few seconds of motion belong to different layers. |
| global and local planning are separated | This shows why complex real problems are not solved all at once. | Understand that one plan chooses the large direction and another chooses the immediate action. |
| path and trajectory should not be mixed | This reduces confusion when reading robotics or autonomous-driving material later. | Understand that `where to pass` and `how to move through time` are different questions. |

A short role split is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| waypoint | a sequence of reference points to pass through | a unit for expressing the larger flow |
| global planner | the layer that decides the larger route to the destination | decides which road and lane flow to follow |
| local planner | the layer that chooses the short motion to execute now | compares immediate trajectory candidates |
| path | the spatial flow of where to pass | expresses the larger movement direction |
| trajectory | a plan that includes time and speed | expresses the immediate movement before execution |
| layering | dividing the problem into different resolutions | the frame that makes a large planning problem manageable |

## Classical Route Finding Is Abstracted as Graph Search

Poole and Mackworth explain that goal achievement can be abstracted as finding a path from a start node to a goal node. In this view, what matters is not the whole world, but which nodes can be reached from the current one and what path leads to the goal.

The route-finding problem can be written simply like this:

| Element | Route-finding example |
| --- | --- |
| node | intersection, position, segment entry point |
| edge | road segment that can be traversed |
| cost | distance, time, energy, traffic condition |
| goal | arrival at destination |
| result | a path to the destination |

This abstraction works well for navigation too. Given a start and destination, the system chooses which roads to follow.

But a real vehicle needs another level below that:

> choosing which road to pass through does not by itself decide  
> how much steering to apply now,  
> how to adjust speed,  
> or how to avoid nearby obstacles

At that point, autonomous-driving path planning refines the classical route-finding problem into additional layers.

## Historically, the Large Route and Immediate Action Became Separated

Early AI and robotics planning often treated `how to reach the goal` as a relatively abstract path problem. But real vehicles and robots do not move only on an abstract graph. They face lanes, curvature, steering limits, other cars, pedestrians, signals, and stop lines.

So practical driving systems naturally developed a separation like this:

| Layer | Central question |
| --- | --- |
| large-route planning | through which roads and lane flows should the vehicle travel to the destination? |
| immediate-motion planning | during the next few seconds, what line and speed profile should the vehicle follow? |
| control | how should that plan be turned into steering and acceleration commands? |

This separation is not a special invention unique to autonomous driving. It is a common form of layering that appears when a complex real problem is too hard to solve all at once.

> the problem of seeing far ahead  
> and the problem of moving right now  
> are hard to solve at the same resolution,  
> so the representation levels get separated

## Waypoints Help Represent the Larger Route

In this flow, `waypoints` can be understood as reference points that should be passed through. Their exact use differs by system, but the core idea here is:

> a waypoint is a representation that lets the larger route be handled  
> as a sequence of reference points

Waypoints can serve several roles:

| Role of waypoints | Explanation |
| --- | --- |
| representing the large route | they give reference points for where the vehicle should pass |
| supporting route following | they show the general directional flow to follow |
| approximating lane centerlines | they turn map geometry into a sequence of manageable points |
| providing a reference for local planning | they give a baseline when short trajectory candidates are built |

The important caution is that waypoints do not automatically equal the full real movement.

| Expression | Core meaning |
| --- | --- |
| waypoint | reference point to pass |
| route or path | the larger flow connecting those points |
| trajectory | a movement plan that also includes time, speed, and acceleration |

So when people say `follow the waypoints`, the stricter reading is often:

> use the waypoints or reference line  
> to build an actual trajectory suited to the current situation

## DARPA-Era Examples Are Often Used as a Turning Point

In the history of autonomous driving, the DARPA Grand Challenge and Urban Challenge are often mentioned. It is safer to read them not as the moment autonomous driving was fully solved, but as cases that made it widely visible that real vehicles must combine route representation, obstacle avoidance, and control together.

In Urban Challenge-era documents and the later research flow, representations such as road networks, lanes, segments, and checkpoints became more structured. Through that period, autonomous-driving discussion moved more clearly toward questions like:

- how should the road network and lane flow be represented?
- how should a large route be found on top of that representation?
- how should short movement candidates be generated under current local conditions?

The DARPA example here is used for historical orientation, not to imply that every current system uses the same formats or pipeline.

## A Global Planner Chooses the Large Route

A `global planner` usually computes the larger route from the start to the destination. It uses relatively long-horizon information such as the map, road connectivity, lane relations, intersections, and traffic-allowed conditions.

The safe introductory reading is:

> the global planner decides  
> which overall road and lane flow to follow to the destination

Its output can appear in several forms:

- a sequence of road segments
- a reference path along lane centerlines
- a sequence of waypoints

So the core role of the global planner is not to decide the exact steering angle at every instant, but to decide which overall flow the vehicle should follow.

## A Local Planner Chooses the Short Trajectory to Execute Now

A `local planner` is not just a module that copies the global route. It uses the current vehicle state, nearby obstacles, lane boundaries, speed conditions, and safety constraints to decide a short trajectory that can be executed now.

Many descriptions of modern motion planning treat the process like this:

| Common stage in local planning | Explanation |
| --- | --- |
| check the reference line | read the road centerline or global route |
| generate candidates | build several short trajectory candidates |
| evaluate candidates | compare collision risk, smoothness, comfort, and constraint satisfaction |
| choose one | decide the trajectory to execute now |
| hand off to tracking or control | turn it into steering and acceleration commands |

The key is that local planning is not only `predicting`. Its central job is:

> create short trajectory candidates, compare them,  
> and choose what to execute now

Predictions about surrounding cars or pedestrians can be important inputs into that process. But many systems still separate prediction from planning: prediction asks `how might others move?`, while planning asks `how should we move in response?`

## Path and Trajectory Should Be Kept Separate

One of the most common confusions in this topic is using `path` and `trajectory` as if they were the same.

Separating them also makes the roles of global and local planning clearer:

| Distinction | Question | Example |
| --- | --- | --- |
| path or route | where should we pass? | which road or lane should we follow? |
| trajectory | when and at what speed should we move? | over the next 3 seconds, should we slow down and avoid left smoothly? |

A `path` is closer to spatial flow, while a `trajectory` includes temporal planning as well.

That is why the following summary is relatively safe:

- the global planner creates the large path
- the local planner uses that path as reference and creates a short trajectory
- the controller turns that trajectory into real steering and acceleration commands

## Reading This Example Again Through Search and Heuristics

If we rewrite the case in the vocabulary of Chapter 7:

| General concept in P1-7 | Corresponding role in autonomous-driving planning |
| --- | --- |
| search space | possible routes, lane choices, and short driving candidates |
| cost | distance, time, safety, comfort, collision risk, constraint violation |
| heuristic | standards that reduce which candidates are inspected first, reference-route-based candidate generation, early removal of high-risk candidates |
| good-enough solution | a safe and executable trajectory found within limited time |
| layering | separation into global path, local trajectory, and control |

The important point is not that autonomous driving is a completely different species of problem. It is that route planning there can still be understood as a large real-world search problem that becomes manageable only after being broken into better representations and layers.

## Checklist

- You can explain the relation between classical route finding and autonomous-driving path planning as an extension of graph search.
- You can explain a `waypoint` as a representation of reference points that should be passed through.
- You can explain the role difference between a `global planner` and a `local planner`.
- You can explain why `path` and `trajectory` should not be used as if they were the same.
- You can reread autonomous-driving planning through `search space`, `cost`, `heuristic`, and `layering`.
- You can separate deciding the large route, choosing the short trajectory, and turning that plan into actual control.
- You can read the autonomous-driving example as a case of planning layers and concept mapping rather than as a section about autonomous driving itself.

## Sources and Further Reading

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., 3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-29.
- DARPA, [DARPA Urban Challenge, Route Network Definition File (RNDF) and Mission Data File (MDF) Formats](https://web.archive.org/web/20130224095708/https://archive.darpa.mil/grandchallenge/docs/RNDF_MDF_Formats_031407.pdf){: target="_blank" rel="noopener noreferrer" }, 2007-03-14, accessed 2026-06-29.
- Siyu Teng, Xuemin Hu, Peng Deng, Bai Li, Yuchen Li, Dongsheng Yang, Yunfeng Ai, Lingxi Li, Zhe Xuanyuan, Fenghua Zhu, Long Chen, [Motion Planning for Autonomous Driving: The State of the Art and Future Perspectives](https://arxiv.org/abs/2303.09824){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023-03-17, accessed 2026-06-29.
- Yuncheng Jiang, Xiaofeng Jin, Yanfei Xiong, Zhaoyong Liu, [A Dynamic Motion Planning Framework for Autonomous Driving in Urban Environments](https://arxiv.org/abs/1912.04458){: target="_blank" rel="noopener noreferrer" }, arXiv, 2019-12-10, accessed 2026-06-29.
