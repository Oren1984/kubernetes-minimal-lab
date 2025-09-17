{{- define "kubernetes-minimal.name" -}}
k8s-minimal
{{- end -}}

{{- define "kubernetes-minimal.fullname" -}}
{{ include "kubernetes-minimal.name" . }}
{{- end -}}
