"use client"

import { useState } from "react"
import { ChevronRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function ToolSelector() {
  const [selectedTool, setSelectedTool] = useState<string>("")

  const handleConnect = () => {
    if (selectedTool) {
      console.log(`Connecting to ${selectedTool}...`)
      // Add your connection logic here
    }
  }

  return (
    <div className="flex items-center gap-3 w-full max-w-md">
      <Select onValueChange={setSelectedTool} value={selectedTool}>
        <SelectTrigger className="rounded-full">
          <SelectValue placeholder="Select a tool" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="github">MatLab</SelectItem>
          <SelectItem value="slack">Simulink</SelectItem>
          <SelectItem value="notion">GitHub</SelectItem>
          <SelectItem value="figma">Figma</SelectItem>
          <SelectItem value="jira">Jira</SelectItem>
          <SelectItem value="asana">Asana</SelectItem>
        </SelectContent>
      </Select>
      <Button onClick={handleConnect} disabled={!selectedTool} className="rounded-full">
        Connect
        <ChevronRight className="ml-1 h-4 w-4" />
      </Button>
    </div>
  )
}
