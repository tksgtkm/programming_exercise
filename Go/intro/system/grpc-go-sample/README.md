# gRPC + Go サンプル

Unary RPC と Server Streaming RPC を実装した最小構成の Greeter サービスです。

## ディレクトリ構成

```
grpc-go-sample/
├── proto/
│   └── greeter.proto      # サービス定義（IDL）
├── gen/
│   └── greeterpb/         # protoc が生成するコードの出力先
├── server/
│   └── main.go            # gRPC サーバー
├── client/
│   └── main.go            # gRPC クライアント
├── go.mod
└── README.md
```

## セットアップ

### 0. モジュールの初期化

新規に始める場合はモジュールを初期化します。**ここで指定するモジュール名が import パスの接頭辞になります。** コード内の import（例: `example.com/grpc-go-sample/gen/greeterpb`）、proto の `option go_package`、この `go mod init` の引数の3か所を必ず同じ接頭辞に揃えてください。ずれると内部パッケージが外部モジュール扱いされ、`404 Not Found` で解決に失敗します。

```bash
go mod init example.com/grpc-go-sample
```

> 将来 GitHub に公開するなら、最初から `github.com/<user>/grpc-go-sample` のように実際のパスで作っておくと、後でリネームせずに済みます。

### 1. ツールのインストール

```bash
# protoc 本体（Ubuntu の場合）
sudo apt install -y protobuf-compiler

# Go 用のコード生成プラグイン
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest

# プラグインが PATH に通っていることを確認（シェルを開き直すと消えるので、
# 恒久化するなら ~/.bashrc などに追記する）
export PATH="$PATH:$(go env GOPATH)/bin"
```

### 2. コード生成

プロジェクトルートで実行します。`--go_opt=module=...` に渡すモジュール名は、手順0で初期化したものと一致させます。`option go_package` のフルパスから接頭辞を取り除いた残り（`gen/greeterpb`）が出力先ディレクトリになります。

```bash
protoc \
  --go_out=. --go_opt=module=example.com/grpc-go-sample \
  --go-grpc_out=. --go-grpc_opt=module=example.com/grpc-go-sample \
  proto/greeter.proto
```

`gen/greeterpb/` 配下に `greeter.pb.go`（メッセージ型）と
`greeter_grpc.pb.go`（サービスのインターフェース／スタブ）が生成されます。生成されたことを確認します。

```bash
ls gen/greeterpb/
# greeter.pb.go  greeter_grpc.pb.go
```

> **順序が重要**: コード生成（手順2）→ 依存解決（手順3）の順で行います。生成物が無いまま `go mod tidy` すると、内部パッケージが見つからず解決に失敗します。

### 3. 依存解決

import を辿って依存を `go.mod` に記録し、`go.sum` を生成します。

```bash
go mod tidy
```

> **Go のバージョン要件について**: gRPC など依存ライブラリが手元より新しい Go を要求する場合があります（例: `go.mod requires go >= 1.25.0`）。`GOTOOLCHAIN=auto` にしておくと、必要なツールチェインを自動取得してくれます。
>
> ```bash
> go env -w GOTOOLCHAIN=auto
> ```
>
> Go を上げたくない場合は、手元の Go で動く旧バージョンを明示的に固定する方法もあります（例: `go get google.golang.org/grpc@v1.71.1`）。
>
> なお `go.sum` を削除してしまっても、`go.mod` が正しければ `go mod tidy` で再生成できます。

## 実行

ターミナルを2つ開いて:

```bash
# ターミナル1: サーバー起動
go run ./server

# ターミナル2: クライアント実行
go run ./client
```

クライアント側の出力例:

```
[Unary] Hello, Takumi!
[Stream] Hello, Takumi!
[Stream] こんにちは, Takumi!
[Stream] Bonjour, Takumi!
[Stream] Hola, Takumi!
[Stream] Ciao, Takumi!
done
```

> **ビルドエラーの切り分け**: `go mod tidy` や `go run` は対象パッケージをまとめて解決するため、一部に問題があると全体が止まります。原因を絞りたいときは `go build ./...`（全体）やパッケージ単位の `go build ./server` を使うと特定しやすいです。

## grpcurl で叩く（おまけ）

サーバーで reflection を有効にしているので、grpcurl から直接呼べます。

```bash
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext -d '{"name": "Takumi"}' localhost:50051 greeter.v1.Greeter/SayHello
grpcurl -plaintext -d '{"name": "Takumi"}' localhost:50051 greeter.v1.Greeter/SayHelloStream
```

## ポイント解説

- **`UnimplementedGreeterServer` の埋め込み**: proto に RPC を追加してもサーバー実装側がコンパイルエラーにならないための前方互換性の仕組み。生成コードが要求します。
- **エラーは `status.Error(codes.Xxx, ...)` で返す**: gRPC のステータスコード（`InvalidArgument`, `NotFound`, `Unavailable` など）にマップされ、クライアント側で `status.FromError()` により判別できます。
- **`context` によるデッドライン伝播**: クライアントの `context.WithTimeout` はメタデータとしてサーバーに伝わり、ストリーミング中でも `stream.Context().Err()` で検知できます。
- **`grpc.NewClient`**: v1.63 以降の推奨 API です（従来の `grpc.Dial` は非推奨化の流れ）。接続は遅延確立され、最初の RPC 時に実際に張られます。
- **reflection**: 開発時のデバッグ用。本番では無効化するか、認可と組み合わせるのが一般的です。

## トラブルシューティング

| 症状 | 原因と対処 |
| --- | --- |
| `unrecognized import path "example.com/..."` / `404 Not Found` | モジュール名と import パスの接頭辞が不一致。`go.mod` の `module` 行を import に合わせる（`go mod edit -module=example.com/grpc-go-sample`）。 |
| `missing go.sum entry for module ...` | 依存が未解決。`go mod tidy` を実行。 |
| `go.mod requires go >= 1.xx.0 (running go 1.yy.0; GOTOOLCHAIN=local)` | 依存が新しい Go を要求。`go env -w GOTOOLCHAIN=auto` で自動取得させるか、旧バージョンの依存を固定する。 |
| `no required module provides package .../gen/greeterpb` | 生成物が無い／場所がずれている。手順2のコード生成を実行し、`ls gen/greeterpb/` で確認。 |