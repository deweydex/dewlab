// Step 3 of refactor/PLAN.md: the runtime's saved-work keys were
// `dewlab:<kind>:<module>:<slug>`; they become `dewlab:<kind>:<id>`. This
// runs once per page load, before anything reads a key, and renames the
// keys that belong to this page's old address. Kept here so it can be read
// on its own; it is pasted into tutorial-runtime.js in step 3 (and the
// vendor bundle rebuilt), not imported from here.
//
// `manifest.legacy` is the old `module:slug` the build writes for every
// migrated tutorial (and, for the one renamed id, the old slug too); a
// tutorial written after the change has no `legacy` and this does nothing.

function migrateStorage(manifest) {
  if (!manifest || !manifest.legacy || !manifest.id) return;
  let store;
  try { store = window.localStorage; } catch (err) { return; }
  const oldSuffix = ":" + manifest.legacy;      // e.g. ":computational-methods:first-steps"
  const newSuffix = ":" + manifest.id;          // e.g. ":first-steps-cm"
  const renames = [];
  for (let i = 0; i < store.length; i += 1) {
    const key = store.key(i);
    if (key && key.startsWith("dewlab:") && key.endsWith(oldSuffix)) {
      renames.push(key);
    }
  }
  for (const key of renames) {
    const next = key.slice(0, -oldSuffix.length) + newSuffix;
    if (store.getItem(next) === null) {
      // Never overwrite work saved under the new key already: a reader who
      // has used the new address since the change keeps that.
      store.setItem(next, store.getItem(key));
    }
    store.removeItem(key);
  }
}
