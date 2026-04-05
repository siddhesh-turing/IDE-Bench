function unflattenObject(flattenedObj) {
  if (typeof flattenedObj !== "object" || flattenedObj === null) {
    throw new Error("Input must be an object");
  }

  let result = {};

  for (let key in flattenedObj) {
    // Regex to handle keys like settings['app.mode'] and settings[app.mode]
    let keys = key
      .match(/([^[\].]+|\[[^\]]*\])/g) // Match segments like 'key', '[inner.key]', etc.
      .map((k) => k.replace(/\[|\]/g, "")) // Clean up the square brackets
      .map((k) => k.replace(/^['"]|['"]$/g, "")); // Remove quotes around the keys

    let current = result;

    for (let i = 0; i < keys.length; i++) {
      let part = isNaN(keys[i]) ? keys[i] : Number(keys[i]);

      if (i === keys.length - 1) {
        current[part] = flattenedObj[key];
      } else {
        if (!current[part] || typeof current[part] !== "object") {
          current[part] = isNaN(keys[i + 1]) ? {} : [];
        }
        current = current[part];
      }
    }
  }

  return result;
}

module.exports = { unflattenObject };