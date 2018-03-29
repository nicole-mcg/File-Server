exports.cls = function(reactInstance, subName=null, modifiers=null) {
	if (reactInstance == null) return;
	var base = reactInstance.constructor.name.split(".").join("-");
	base = subName != null && subName !== "" ? base + "-" + subName : base;
	var output = []
	output[0] = base
	if (modifiers != null) {
		for (var key of Object.keys(modifiers)) {
			if (modifiers[key] != undefined && modifiers[key]) {
				output.push(base + "--" + key);
			}
		}
	}
	return output.join(" ");
};

exports.constants = {
    SMALL: "small",
    MEDIUM: "medium",
    LARGE: "large",
}