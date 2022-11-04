# SMEPy
Python version of Structure Mapping Engine (SME). 

Run 
```bash
cd smepy
python flow_example.py
```

on a Gripper and Ferry domains.

The encodings of domains are in `smepy/examples`:
  - the folder `domains` contains all domains from PG# in the most basic encoding
  - the folder `domains_altrepr` contains thedomains in an alternative representation

The SME encodings are always in `.meld` files.


# How to read the output

the SME script will output something like this
```
expression mappings:
(<(not (apply2 carry d-obj d-gripper)), 1.0> -- <(not (apply1 on d-car)), 1.0>),
(<(not (apply2 at p-obj p-room)), 1.0> -- <(not (apply2 at b-car b-loc)), 1.0>),
(<(apply1 ball d-obj), 1.0> -- <(apply1 car d-car), 1.0>),
(<(param drop d-obj), 1.0> -- <(param debark d-car), 1.0>),
(<(param pick p-obj), 1.0> -- <(param board b-car), 1.0>),
(<(apply1 room p-room), 1.0> -- <(apply1 location b-loc), 1.0>),
(<(action drop), 1.0> -- <(action debark), 1.0>),
(<(param move m-to), 1.0> -- <(param sail s-to), 1.0>),
(<(precon move (apply1 room m-from)), 1.0> -- <(precon sail (apply1 location s-from)), 1.0>),
(<(param pick p-room), 1.0> -- <(param board b-loc), 1.0>),
(<(precon pick (apply1 at-robby p-room)), 1.0> -- <(precon board (apply1 at-ferry b-loc)), 1.0>),
(<(not (apply1 at-robby m-from)), 1.0> -- <(not (apply1 at-ferry s-from)), 1.0>),
(<(apply2 at p-obj p-room), 1.0> -- <(apply2 at b-car b-loc), 1.0>),
(<(effect drop (not (apply2 carry d-obj d-gripper))), 1.0> -- <(effect debark (not (apply1 on d-car))), 1.0>),
(<(precon move (apply1 room m-to)), 1.0> -- <(precon sail (apply1 location s-to)), 1.0>),
(<(precon pick (apply1 ball p-obj)), 1.0> -- <(precon board (apply1 car b-car)), 1.0>),
(<(effect pick (not (apply1 free p-gripper))), 1.0> -- <(effect board (not (apply0 empty-ferry))), 1.0>),
(<(apply1 at-robby m-from), 1.0> -- <(apply1 at-ferry s-from), 1.0>),
(<(apply1 at-robby m-to), 1.0> -- <(apply1 at-ferry s-to), 1.0>),
(<(precon pick (apply1 room p-room)), 1.0> -- <(precon board (apply1 location b-loc)), 1.0>),
(<(apply1 room d-room), 1.0> -- <(apply1 location d-loc), 1.0>),
(<(apply1 ball p-obj), 1.0> -- <(apply1 car b-car), 1.0>),
(<(not (apply1 free p-gripper)), 1.0> -- <(not (apply0 empty-ferry)), 1.0>),
(<(effect move (apply1 at-robby m-to)), 1.0> -- <(effect sail (apply1 at-ferry s-to)), 1.0>),
(<(action move), 1.0> -- <(action sail), 1.0>),
(<(effect pick (not (apply2 at p-obj p-room))), 1.0> -- <(effect board (not (apply2 at b-car b-loc))), 1.0>),
(<(effect drop (apply2 at d-obj d-room)), 1.0> -- <(effect debark (apply2 at d-car d-loc)), 1.0>),
(<(precon pick (apply2 at p-obj p-room)), 1.0> -- <(precon board (apply2 at b-car b-loc)), 1.0>),
(<(param move m-from), 1.0> -- <(param sail s-from), 1.0>),
(<(apply1 room m-to), 1.0> -- <(apply1 location s-to), 1.0>),
(<(precon drop (apply1 at-robby d-room)), 1.0> -- <(precon debark (apply1 at-ferry d-loc)), 1.0>),
(<(precon move (apply1 at-robby m-from)), 1.0> -- <(precon sail (apply1 at-ferry s-from)), 1.0>),
(<(apply1 at-robby p-room), 1.0> -- <(apply1 at-ferry b-loc), 1.0>),
(<(apply1 at-robby d-room), 1.0> -- <(apply1 at-ferry d-loc), 1.0>),
(<(effect move (not (apply1 at-robby m-from))), 1.0> -- <(effect sail (not (apply1 at-ferry s-from))), 1.0>),
(<(apply2 at d-obj d-room), 1.0> -- <(apply2 at d-car d-loc), 1.0>),
(<(param drop d-room), 1.0> -- <(param debark d-loc), 1.0>),
(<(precon drop (apply1 ball d-obj)), 1.0> -- <(precon debark (apply1 car d-car)), 1.0>),
(<(action pick), 1.0> -- <(action board), 1.0>),
(<(apply1 room m-from), 1.0> -- <(apply1 location s-from), 1.0>)

entity mappings:
(<m-to> -- <s-to>), (<d-obj> -- <d-car>), (<m-from> -- <s-from>), (<p-room> -- <b-loc>), (<drop> -- <debark>), (<move> -- <sail>), (<d-room> -- <d-loc>), (<ball> -- <car>), (<at-robby> -- <at-ferry>), (<p-obj> -- <b-car>), (<room> -- <location>), (<pick> -- <board>), (<at> -- <at>)

15.385000000000016
```
The first block, `expression mappings`, lists the equivalent/align expressions in the two domains (source -- target). They define correspondences between predicates. One tuple == one match.

The second block, `entity mappings`, lists the correspondence between entities in the two domains. One tuple = one match.

For some reason, the expressions sometimes imply more correspondences then the entities. I'm not sure why exactly.
