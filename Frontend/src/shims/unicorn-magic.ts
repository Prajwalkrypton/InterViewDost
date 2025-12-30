// Shim for the `unicorn-magic` package to satisfy esbuild/Vite in the browser.
// The real functionality is only needed in Node CLI tools; for a web app we
// can safely provide simple identity helpers.

export function toPath(path: string): string {
  return path;
}

export function traversePathUp(path: string): string {
  return path;
}

export default {
  toPath,
  traversePathUp,
};
