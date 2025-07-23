{{/*
Home Electricity labels
*/}}
{{- define "home.labels" -}}
app_name: {{ .Chart.Name }}
namespace: {{ .Release.Namespace }}
{{- end -}}