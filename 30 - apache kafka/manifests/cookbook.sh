# TODO switch to helm installation
# !! DO NOT RUN IF KAFKA ALREADY INSTALLED IN CLUSTER !! Not possible to specify version instead of latest
  ##################################kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
# !! DO NOT RUN IF KAFKA ALREADY INSTALLED IN CLUSTER !! Not possible to specify version instead of latest

kubectl apply --namespace kafka -f ../resource-manifests/${anzu_env}/clusters/kafka/kafka-cert.yaml
cecho blue "wait 10 secs" && sleep 10
kubectl -n kafka get secret anzu-kafka-cert -o=go-template='{{index .data "tls.key"}}' | base64 -d > /tmp/kafka-key.crt
kubectl -n kafka get secret anzu-kafka-cert -o=go-template='{{index .data "ca.crt"}}' | base64 -d > /tmp/kafka-ca.crt
kubectl -n kafka create secret generic anzu-cluster-ca-cert --from-file=ca.crt=/tmp/kafka-ca.crt
kubectl -n kafka create secret generic anzu-cluster-ca --from-file=ca.key=/tmp/kafka-key.crt
kubectl -n kafka label secret anzu-cluster-ca-cert strimzi.io/kind=Kafka strimzi.io/cluster=anzu
kubectl -n kafka label secret anzu-cluster-ca strimzi.io/kind=Kafka strimzi.io/cluster=anzu
kubectl apply --namespace kafka -f ../resource-manifests/${anzu_env}/clusters/kafka/kafka-persistent.yaml
kubectl create configmap anzu-kafka-ca-crt --from-file=/tmp/kafka-ca.crt --namespace ${anzu_env}
kubectl apply --namespace kafka -f ../resource-manifests/${anzu_env}/clusters/kafka/kafka-topics.yaml
