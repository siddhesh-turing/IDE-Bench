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
          // BUG FOR LOGICAL ERROR: Always create arrays instead of checking next key type - this will create arrays where objects are expected, causing data structure issues
          current[part] = [];
        }
        current = current[part];
      }
    }
  }

  return result;
}

module.exports = { unflattenObject }; 


describe(`Testing responses`, () => {
  test("test_HC should convert a simple flattened object into a nested object", () => {
    const obj = {
      "user.name": "Alice",
      "user.age": 25,
      "user.address.city": "New York",
      "user.address.zip": "10001",
    };

    expect(unflattenObject(obj)).toEqual({
      user: {
        name: "Alice",
        age: 25,
        address: {
          city: "New York",
          zip: "10001",
        },
      },
    });
  });

  test("test_EC should return an empty object when given an empty object", () => {
    expect(unflattenObject({})).toEqual({});
  });

  test("test_HC should correctly handle nested arrays", () => {
    const obj = {
      "users.0.name": "Alice",
      "users.0.age": 25,
      "users.1.name": "Bob",
      "users.1.age": 30,
    };

    expect(unflattenObject(obj)).toEqual({
      users: [
        { name: "Alice", age: 25 },
        { name: "Bob", age: 30 },
      ],
    });
  });

  test("test_EC should correctly handle keys with special characters", () => {
    const obj = {
      "user.profile@info.name": "Alice",
      "user.profile@info.age": 25,
    };

    expect(unflattenObject(obj)).toEqual({
      user: {
        "profile@info": {
          name: "Alice",
          age: 25,
        },
      },
    });
  });

  test("test_HC should correctly handle a mix of numeric and string keys", () => {
    const obj = {
      "data.0": "first",
      "data.1": "second",
      "meta.version": 1,
    };

    expect(unflattenObject(obj)).toEqual({
      data: ["first", "second"],
      meta: { version: 1 },
    });
  });

  test("test_EC should throw an error when input is not an object", () => {
    expect(() => unflattenObject(null)).toThrow();
    expect(() => unflattenObject(undefined)).toThrow();
    expect(() => unflattenObject("invalid")).toThrow();
    expect(() => unflattenObject(123)).toThrow();
  });

  test("test_HC should correctly handle mixed-depth nesting", () => {
    const obj = {
      "settings.theme": "dark",
      "settings.notifications.email": true,
      "settings.notifications.push": false,
      "user.profile.name": "Alice",
      "user.profile.age": 25,
    };

    expect(unflattenObject(obj)).toEqual({
      settings: {
        theme: "dark",
        notifications: {
          email: true,
          push: false,
        },
      },
      user: {
        profile: {
          name: "Alice",
          age: 25,
        },
      },
    });
  });

  test("test_HC should correctly handle keys with undefined or null values", () => {
    const obj = {
      "config.mode": "test",
      "config.timeout": null,
      "config.retries": undefined,
    };

    expect(unflattenObject(obj)).toEqual({
      config: {
        mode: "test",
        timeout: null,
        retries: undefined,
      },
    });
  });

  test("test_HC should handle deeply nested structures", () => {
    const obj = {
      "a.b.c.d.e.f.g": "deep",
      "x.y.z": 100,
    };

    expect(unflattenObject(obj)).toEqual({
      a: {
        b: {
          c: {
            d: {
              e: {
                f: {
                  g: "deep",
                },
              },
            },
          },
        },
      },
      x: {
        y: {
          z: 100,
        },
      },
    });
  });

  test("test_HC should handle objects with mixed types at different levels", () => {
    const obj = {
      "project.name": "AI System",
      "project.tasks.0.title": "Build Model",
      "project.tasks.0.completed": false,
      "project.tasks.1.title": "Test Model",
      "project.tasks.1.completed": true,
      "project.details.owner": "Alice",
    };

    expect(unflattenObject(obj)).toEqual({
      project: {
        name: "AI System",
        tasks: [
          { title: "Build Model", completed: false },
          { title: "Test Model", completed: true },
        ],
        details: {
          owner: "Alice",
        },
      },
    });
  });

  test("test_HC should handle deeply nested keys with array indexes in different locations", () => {
    const obj = {
      "company.departments.0.name": "Engineering",
      "company.departments.0.employees.0.name": "Alice",
      "company.departments.0.employees.1.name": "Bob",
      "company.departments.1.name": "HR",
      "company.departments.1.employees.0.name": "Charlie",
    };

    expect(unflattenObject(obj)).toEqual({
      company: {
        departments: [
          {
            name: "Engineering",
            employees: [{ name: "Alice" }, { name: "Bob" }],
          },
          {
            name: "HR",
            employees: [{ name: "Charlie" }],
          },
        ],
      },
    });
  });

  test("test_EC should handle keys containing dots inside brackets", () => {
    const obj = {
      "settings['app.mode']": "production",
      "settings['user.theme']": "dark",
    };

    expect(unflattenObject(obj)).toEqual({
      settings: {
        "app.mode": "production",
        "user.theme": "dark",
      },
    });
  });

  test('performance test: should complete within 120 seconds', () => {
    // Generate large input dynamically:
    // 5000 nested keys with deep nesting for stress testing
    const largeInput = {};
    for (let i = 0; i < 5000; i++) {
      const deepKey = `level${i}.nested${i}.deep${i}.value${i}`;
      largeInput[deepKey] = `data${i}`;
    }

    const startTime = Date.now();
    unflattenObject(largeInput);
    const duration = Date.now() - startTime;

    console.log(`Performance test duration: ${duration} ms`);
    expect(duration).toBeLessThanOrEqual(120000); // 120 seconds
  }, 130000); // Jest timeout set to 130 seconds
});