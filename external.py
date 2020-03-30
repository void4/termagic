from magic import capture_line
from patterns import ImagePatternHandler


line = capture_line()

handler = ImagePatternHandler("commands")

pattern = handler.input_to_pattern(line)

SAVE = False
if SAVE:
	handler.save_pattern(SAVE, pattern)
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
