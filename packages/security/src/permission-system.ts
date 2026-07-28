export enum PermissionLevel {
  Level0_Silent = 0,       // Read workspace files, query memory (Auto-Approved)
  Level1_Workspace = 1,    // Write/edit files inside workspace (Workspace Auto)
  Level2_Notification = 2, // External network requests, package installs (Toast)
  Level3_Consent = 3,      // Delete files, run admin/destructive commands (Interactive User Consent Prompt)
}

export interface SecurityEvaluation {
  level: PermissionLevel;
  requiresConsent: boolean;
  reason: string;
}

export class PermissionGatekeeper {
  constructor(private workspacePath: string = process.cwd()) {}

  evaluateToolCall(toolName: string, args: Record<string, unknown>): SecurityEvaluation {
    switch (toolName) {
      case 'read_file':
      case 'list_directory':
        return {
          level: PermissionLevel.Level0_Silent,
          requiresConsent: false,
          reason: 'Read-only operation inside workspace',
        };

      case 'write_file':
      case 'edit_file': {
        const filePath = String(args.path || '');
        if (this.isInsideWorkspace(filePath)) {
          return {
            level: PermissionLevel.Level1_Workspace,
            requiresConsent: false,
            reason: 'File modification inside active workspace boundary',
          };
        }
        return {
          level: PermissionLevel.Level3_Consent,
          requiresConsent: true,
          reason: 'File modification outside active workspace boundary',
        };
      }

      case 'run_command': {
        const command = String(args.command || '').trim().toLowerCase();

        // Destructive / System Level Commands
        if (
          command.includes('rm -rf') ||
          command.includes('sudo') ||
          command.includes('format') ||
          command.includes('del /f') ||
          command.includes('drop database')
        ) {
          return {
            level: PermissionLevel.Level3_Consent,
            requiresConsent: true,
            reason: 'Destructive command execution requires explicit user authorization',
          };
        }

        return {
          level: PermissionLevel.Level2_Notification,
          requiresConsent: false,
          reason: 'Standard shell command execution',
        };
      }

      default:
        return {
          level: PermissionLevel.Level3_Consent,
          requiresConsent: true,
          reason: 'Unknown tool requires user review',
        };
    }
  }

  private isInsideWorkspace(targetPath: string): boolean {
    if (!targetPath) return false;
    const normalizedTarget = targetPath.replace(/\\/g, '/');
    const normalizedWs = this.workspacePath.replace(/\\/g, '/');
    return normalizedTarget.startsWith(normalizedWs);
  }
}
