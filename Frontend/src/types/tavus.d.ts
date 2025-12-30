declare module "@tavus/cvi-ui" {
  import * as React from "react";

  export const CVIProvider: React.FC<{
    apiKey: string;
    children: React.ReactNode;
  }>;

  export const Conversation: React.FC<{
    conversationUrl: string;
  }>;
}
