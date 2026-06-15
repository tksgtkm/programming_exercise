protoc \
  --go_out=. --go_opt=module=example.com/grpc-order \
  --go-grpc_out=. --go-grpc_opt=module=example.com/grpc-order \
  proto/order_management.proto