import { exec } from 'node:child_process';
import { promisify } from 'node:util';

const execAsync = promisify(exec);

export interface TerminalCallResult {
  success: boolean;
  stdout: string;
  stderr: string;
  exitCode: number;
  error?: string;
}

export class TerminalMcpServer {
  async runCommand(command: string, cwd: string = process.cwd()): Promise<TerminalCallResult> {
    if (!command || !command.trim()) {
      return {
        success: false,
        stdout: '',
        stderr: 'Command cannot be empty',
        exitCode: 1,
        error: 'Empty command string',
      };
    }

    try {
      const { stdout, stderr } = await execAsync(command, {
        cwd,
        env: process.env,
        maxBuffer: 10 * 1024 * 1024, // 10MB
      });

      return {
        success: true,
        stdout,
        stderr,
        exitCode: 0,
      };
    } catch (err: unknown) {
      const execError = err as { code?: number; stdout?: string; stderr?: string; message?: string };
      return {
        success: false,
        stdout: execError.stdout || '',
        stderr: execError.stderr || execError.message || String(err),
        exitCode: execError.code || 1,
        error: execError.message || String(err),
      };
    }
  }
}
