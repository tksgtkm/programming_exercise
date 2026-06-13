package main

import (
	"context"
	"errors"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "example.com/grpc-go-sample/gen/greeterpb"
)

func main() {
	conn, err := grpc.NewClient(
		"localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		log.Fatalf("failed to connect: %v", err)
	}
	defer conn.Close()

	client := pb.NewGreeterClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	res, err := client.SayHello(ctx, &pb.HelloRequest{Name: "Takumi"})
	if err != nil {
		log.Fatalf("SayHello failed: %v", err)
	}
	log.Printf("[Unary] %s", res.GetMessage())

	streamCtx, streamCancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer streamCancel()

	stream, err := client.SayHelloStream(streamCtx, &pb.HelloRequest{Name: "Takumi"})
	if err != nil {
		log.Fatalf("SayHelloStream failed: %v", err)
	}
	for {
		msg, err := stream.Recv()
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			log.Fatalf("stream recv failed: %v", err)
		}
		log.Printf("[Stream] %s", msg.GetMessage())
	}

	log.Println("done")
}
