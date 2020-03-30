from mouse import capture_line, enhanced_line
from util import normalize
from patterns import ImagePatternHandler, PathPatternHandler


line = capture_line()

norm = normalize(line)
eline = enhanced_line(norm)

#for coord in eline:
#    print(coord)

handler = PathPatternHandler("commands")#ImagePatternHandler("patterns")

pattern = handler.input_to_pattern(line)

commands = [""]

SAVE = False
name = "b"
if SAVE:
	handler.save_pattern(name, pattern)
	raise RuntimeError("Pattern saved")

closest = handler.closest_pattern(pattern)

if closest is None:
    #save first gesture as "accept" gesture?
    #ex nihilo
    #pattern as name for another pattern
    #referring to sets of patterns with a pattern
    #recognize the structure in everything
    pass
else:
    print(closest["name"])
