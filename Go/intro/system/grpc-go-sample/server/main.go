package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"

	pb "example.com/grpc-go-sample/gen/greeterpb"
)

type greeterServer struct {
	pb.UnimplementedGreeterServer
}

func (s *greeterServer) SayHello(ctx context.Context, req *pb.HelloRequest) (*pb.HelloReply, error) {
	name := req.GetName()
	if name == "" {
		return nil, status.Error(codes.InvalidArgument, "name must not be empty")
	}
	log.Printf("SayHello called: name=%q", name)
	return &pb.HelloReply{
		Message: fmt.Sprintf("Hello, %s!", name),
	}, nil
}

func (s *greeterServer) SayHelloStream(req *pb.HelloRequest, stream pb.Greeter_SayHelloStreamServer) error {
	name := req.GetName()
	if name == "" {
		return status.Error(codes.InvalidArgument, "name must not be empty")
	}
	log.Printf("SayHelloStream called: name=%q", name)

	greetings := []string{"Hello", "こんにちは", "Bonjour", "Hola", "Ciao"}

	for _, g := range greetings {
		if err := stream.Context().Err(); err != nil {
			return status.FromContextError(err).Err()
		}
		if err := stream.Send(&pb.HelloReply{
			Message: fmt.Sprintf("%s, %s!", g, name),
		}); err != nil {
			return err
		}
		time.Sleep(500 * time.Millisecond)
	}
	return nil
}

func main() {
	const addr = ":50051"

	lis, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &greeterServer{})

	reflection.Register(s)

	log.Printf("gRPC server listening on %s", addr)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
