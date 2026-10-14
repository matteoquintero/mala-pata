/**
 * mala-pata-notify — OpenCode adapter
 *
 * Bridges OpenCode's event system to the agent-agnostic `mala-pata-notify`
 * entrypoint (same desktop overlay + sound used by Claude Code, Codex, Kimi
 * and Gemini). OpenCode has no declarative command hook, so this thin plugin
 * is the shim: it maps OpenCode events to the entrypoint.
 *
 *   session.idle      -> --event finished   (the agent went idle / finished)
 *   permission.asked  -> --event waiting     (the agent is waiting on the user)
 *
 * OpenCode delivers events in-process (not stdin JSON), so we hand the
 * entrypoint a minimal payload via --argv-json carrying cwd; the entrypoint's
 * universal fallback (basename(cwd) + git branch + agent + time) does the rest.
 *
 * Failure policy: best-effort. It must NEVER block OpenCode nor throw into the
 * host — every path is guarded and the child is detached.
 */
import type { Plugin } from "@opencode-ai/plugin"
import { execFile } from "node:child_process"
import { homedir } from "node:os"
import { join } from "node:path"

const NOTIFY = join(homedir(), ".mala-pata", "bin", "mala-pata-notify")

export const MalaPataNotifyPlugin: Plugin = async (input) => {
  const directory =
    (input as { directory?: string } | undefined)?.directory ?? process.cwd()

  const fire = (event: "finished" | "waiting") => {
    try {
      const child = execFile(
        NOTIFY,
        [
          "--event", event,
          "--agent", "opencode",
          "--argv-json", JSON.stringify({ cwd: directory }),
        ],
        { timeout: 5000 },
      )
      child.on("error", () => {})
      child.unref?.()
    } catch {
      /* best-effort: never block or throw into the host */
    }
  }

  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") fire("finished")
      else if (event.type === "permission.asked") fire("waiting")
    },
  }
}

export default MalaPataNotifyPlugin
