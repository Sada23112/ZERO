import { describe, it, expect } from 'vitest';
import { PermissionGatekeeper, PermissionLevel } from '../src/index.js';
import path from 'node:path';

describe('Milestone 15: Security Permission Gatekeeper', () => {
  const wsPath = process.cwd();
  const gatekeeper = new PermissionGatekeeper(wsPath);

  it('should auto-approve read_file (Level 0)', () => {
    const evalRes = gatekeeper.evaluateToolCall('read_file', { path: 'package.json' });
    expect(evalRes.level).toBe(PermissionLevel.Level0_Silent);
    expect(evalRes.requiresConsent).toBe(false);
  });

  it('should auto-approve workspace file edits (Level 1)', () => {
    const evalRes = gatekeeper.evaluateToolCall('write_file', { path: path.join(wsPath, 'src/test.ts') });
    expect(evalRes.level).toBe(PermissionLevel.Level1_Workspace);
    expect(evalRes.requiresConsent).toBe(false);
  });

  it('should require interactive user consent for destructive commands (Level 3)', () => {
    const evalRes = gatekeeper.evaluateToolCall('run_command', { command: 'rm -rf /' });
    expect(evalRes.level).toBe(PermissionLevel.Level3_Consent);
    expect(evalRes.requiresConsent).toBe(true);
  });
});
