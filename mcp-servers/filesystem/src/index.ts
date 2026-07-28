export { FilesystemMcpServer, ToolCallRequest, ToolCallResult } from './filesystem-server.js';

export function getFilesystemMcpInfo(): string {
  return 'Project ZERO Filesystem MCP Tool Server (read_file, write_file, edit_file, list_directory) Active';
}
