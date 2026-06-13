protoc \
  --go_out=. --go_opt=module=example.com/grpc-ecommerce \
  --go-grpc_out=. --go-grpc_opt=module=example.com/grpc-ecommerce \
  proto/product_info.proto