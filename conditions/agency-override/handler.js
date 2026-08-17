// Soul Override Hook for Victor
// Injects AGENCY-OVERRIDE.md after SOUL.md in bootstrap context

import { readFile } from "fs/promises";
import { join } from "path";

const HOOK_NAME = "soul-override";
const OVERRIDE_FILENAME = "AGENCY-OVERRIDE.md";

async function soulOverrideHook(event) {
  // Only act on agent:bootstrap events
  if (!event.context) return;
  
  const workspaceDir = event.context.workspaceDir;
  if (!workspaceDir) return;
  
  const overridePath = join(workspaceDir, "hooks", HOOK_NAME, OVERRIDE_FILENAME);
  
  let rawContent;
  try {
    rawContent = await readFile(overridePath, "utf-8");
  } catch (err) {
    // File doesn't exist — hook not applicable or misconfigured
    return;
  }
  
  // Add to bootstrap files array, after SOUL.md
  // The entry structure has at least: { path: string }
  // We use the full path as the identifier
  const overrideEntry = {
    path: overridePath,
    raw: rawContent,
    rawSize: rawContent.length
  };
  
  // Insert after existing files — at the end of the bootstrapFiles array
  // This ensures it loads after SOUL.md and has the last word on agency
  if (event.context.bootstrapFiles) {
    event.context.bootstrapFiles.push(overrideEntry);
  }
}

export { soulOverrideHook as default };
