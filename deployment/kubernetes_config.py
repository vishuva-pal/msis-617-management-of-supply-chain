"""
Kubernetes Configuration
K8s manifests for production deployment
"""

class KubernetesConfig:
    """Kubernetes deployment configuration"""
    
    @staticmethod
    def generate_deployment_yaml() -> str:
        """Generate Kubernetes Deployment manifest"""
        return """# ComplianceGuard AI Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: complianceguard-ai
  labels:
    app: complianceguard-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: complianceguard-ai
  template:
    metadata:
      labels:
        app: complianceguard-ai
    spec:
      containers:
      - name: complianceguard-ai
        image: gcr.io/your-project-id/complianceguard-ai:latest
        ports:
        - containerPort: 8080
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: REDIS_HOST
          value: "complianceguard-redis"
        resources:
          requests:
            cpu: "1000m"
            memory: "2Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
---
# Redis Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: complianceguard-redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: complianceguard-redis
  template:
    metadata:
      labels:
        app: complianceguard-redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        persistentVolumeClaim:
          claimName: redis-pvc
---
# Persistent Volume Claim for Redis
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
"""

    @staticmethod
    def generate_service_yaml() -> str:
        """Generate Kubernetes Service manifest"""
        return """# ComplianceGuard AI Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: complianceguard-ai-service
spec:
  selector:
    app: complianceguard-ai
  ports:
  - name: http
    port: 80
    targetPort: 8080
  type: LoadBalancer
---
# Redis Service
apiVersion: v1
kind: Service
metadata:
  name: complianceguard-redis
spec:
  selector:
    app: complianceguard-redis
  ports:
  - port: 6379
    targetPort: 6379
"""

    @staticmethod
    def generate_ingress_yaml() -> str:
        """Generate Kubernetes Ingress manifest"""
        return """# ComplianceGuard AI Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: complianceguard-ai-ingress
  annotations:
    kubernetes.io/ingress.class: "gce"
    networking.gke.io/managed-certificates: complianceguard-certificate
spec:
  rules:
  - host: complianceguard.your-domain.com
    http:
      paths:
      - path: /*
        pathType: ImplementationSpecific
        backend:
          service:
            name: complianceguard-ai-service
            port:
              number: 80
---
# Managed Certificate
apiVersion: networking.gke.io/v1
kind: ManagedCertificate
metadata:
  name: complianceguard-certificate
spec:
  domains:
    - complianceguard.your-domain.com
"""

    @staticmethod
    def generate_hpa_yaml() -> str:
        """Generate Horizontal Pod Autoscaler manifest"""
        return """# ComplianceGuard AI Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: complianceguard-ai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: complianceguard-ai
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""