/* A client of GitHub's own API and nothing else: dewlab has no server to send
 * a change to. Shared by the authoring editor (editor.js) and the in-page
 * editor (inpage-edit.js). The token is one the author pastes in; it stays in
 * this browser's localStorage and needs `contents: write` and `pull requests:
 * write` on this repository, nothing broader. It can propose commits and
 * cannot merge them. */

export const API = "https://api.github.com";
export const TOKEN_KEY = "dewlab:editor:token";
export const REPO = "deweydex/dewlab";

export function githubClient(token) {
  async function call(path, options = {}) {
    const response = await fetch(API + path, {
      ...options,
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...(options.headers || {}),
      },
    });
    if (!response.ok) {
      const detail = await response.text();
      throw new Error(`GitHub said ${response.status}: ${detail.slice(0, 300)}`);
    }
    return response.status === 204 ? null : response.json();
  }

  return {
    async listTutorials() {
      const head = await call(`/repos/${REPO}/git/ref/heads/main`);
      const tree = await call(`/repos/${REPO}/git/trees/${head.object.sha}?recursive=1`);
      return {
        base: head.object.sha,
        paths: tree.tree
          .filter((e) => e.type === "blob"
            && (e.path.startsWith("tutorials/") || e.path.startsWith("courses/")))
          .map((e) => e.path),
      };
    },
    /* The commit `main` is at now, and the blob sha `main` holds for one file. */
    async mainSha() {
      const head = await call(`/repos/${REPO}/git/ref/heads/main`);
      return head.object.sha;
    },
    async fileShaAtMain(path) {
      const file = await call(`/repos/${REPO}/contents/${encodeURI(path)}?ref=main`);
      return file.sha;
    },
    /* A file as it was when the site was built: GitHub serves any blob by its sha. */
    async blob(sha) {
      const blob = await call(`/repos/${REPO}/git/blobs/${sha}`);
      return decodeURIComponent(escape(atob(blob.content.replace(/\n/g, ""))));
    },
    async read(path) {
      const file = await call(`/repos/${REPO}/contents/${encodeURI(path)}?ref=main`);
      return decodeURIComponent(escape(atob(file.content.replace(/\n/g, ""))));
    },
    async commit({ base, branch, message, files }) {
      const blobs = [];
      for (const file of files) {
        if (file.text === null) {
          blobs.push({ path: file.path, mode: "100644", type: "blob", sha: null });
          continue;
        }
        const blob = await call(`/repos/${REPO}/git/blobs`, {
          method: "POST",
          body: JSON.stringify({ content: file.text, encoding: "utf-8" }),
        });
        blobs.push({ path: file.path, mode: "100644", type: "blob", sha: blob.sha });
      }
      const tree = await call(`/repos/${REPO}/git/trees`, {
        method: "POST",
        body: JSON.stringify({ base_tree: base, tree: blobs }),
      });
      const created = await call(`/repos/${REPO}/git/commits`, {
        method: "POST",
        body: JSON.stringify({ message, tree: tree.sha, parents: [base] }),
      });
      await call(`/repos/${REPO}/git/refs`, {
        method: "POST",
        body: JSON.stringify({ ref: `refs/heads/${branch}`, sha: created.sha }),
      });
      const pull = await call(`/repos/${REPO}/pulls`, {
        method: "POST",
        body: JSON.stringify({
          title: message.split("\n")[0],
          head: branch,
          base: "main",
          draft: true,
          body: `Written from the dewlab editor.\n\n${message}`,
        }),
      });
      return pull.html_url;
    },
    /* Another commit on a branch an earlier commit() made, so one editing
     * session stays one pull request. */
    async commitMore({ branch, message, files }) {
      const ref = await call(`/repos/${REPO}/git/ref/heads/${branch}`);
      const tip = ref.object.sha;
      const head = await call(`/repos/${REPO}/git/commits/${tip}`);
      const blobs = [];
      for (const file of files) {
        const blob = await call(`/repos/${REPO}/git/blobs`, {
          method: "POST",
          body: JSON.stringify({ content: file.text, encoding: "utf-8" }),
        });
        blobs.push({ path: file.path, mode: "100644", type: "blob", sha: blob.sha });
      }
      const tree = await call(`/repos/${REPO}/git/trees`, {
        method: "POST",
        body: JSON.stringify({ base_tree: head.tree.sha, tree: blobs }),
      });
      const created = await call(`/repos/${REPO}/git/commits`, {
        method: "POST",
        body: JSON.stringify({ message, tree: tree.sha, parents: [tip] }),
      });
      await call(`/repos/${REPO}/git/refs/heads/${branch}`, {
        method: "PATCH",
        body: JSON.stringify({ sha: created.sha }),
      });
    },
  };
}
