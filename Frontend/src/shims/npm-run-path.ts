// Lightweight shim for `npm-run-path` to satisfy Vite/esbuild bundling.
// The real package is only needed in Node CLI contexts; the browser build
// does not rely on this functionality. We provide no-op/identity versions
// that keep the dependency graph happy.

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
