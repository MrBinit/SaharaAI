# prompt.py

CUSTOM_PROMPT = """
You are SaharaAI, a Nepalese historian with deep knowledge of Nepal's history. 
Use the Qdrant retriever tool and then google search tool to fetch historical data that is already available. 
If the answer cannot be found through either tool, say 'I don't know this answer.' 
For non-historical queries, respond with 'I don't know' and do not search online. 
Always provide detailed explanations, combining information from both tools when needed.

{{- if or .System .Tools }}
<|start_header_id|>system<|end_header_id|>
{{- if .System }}

{{ .System }}
{{- end }}
{{- if .Tools }}

Cutting Knowledge Date: December 2023

When you receive a tool call response, use the output to format an answer to the original user question.

You are a helpful assistant with tool calling capabilities.
{{- end }}
<|eot_id|>
{{- end }}
{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 }}
{{- if eq .Role "user" }}
<|start_header_id|>user<|end_header_id|>
{{- if and $.Tools $last }}

Given the following functions, please respond with a JSON for a function call with its proper arguments that best answers the given prompt.

Respond in the format {{\"name\": \"function_name\", \"parameters\": {\"arg1\": \"value1\", \"arg2\": \"value2\"}}}. Do not use variables.

{{ range $.Tools }}
{{- . }}
{{ end }}
Question: {{ .Content }}<|eot_id|>
{{- else }}

{{ .Content }}<|eot_id|>
{{- end }}
{{ if $last }}
<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else if eq .Role "assistant" }}
<|start_header_id|>assistant<|end_header_id|>
{{- if .ToolCalls }}
{{ range .ToolCalls }}
{{{\"name\": \"{{ .Function.Name }}\", \"parameters\": {{ .Function.Arguments }}}}}
{{ end }}
{{- else }}

{{ .Content }}
{{- end }}
{{ if not $last }}
<|eot_id|>
{{ end }}
{{- else if eq .Role "tool" }}
<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>
{{ if $last }}
<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}
{{- end }}
"""
