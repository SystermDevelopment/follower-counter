#!/bin/bash
# SNSフォロワー数表示アプリ セットアップスクリプト

echo "=== SNSフォロワー数表示アプリ セットアップ ==="

# OSを判定
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
fi

# Raspberry Pi / Debian系の場合
if [[ "$OS" == "raspbian" ]] || [[ "$OS" == "debian" ]] || [[ "$OS" == "ubuntu" ]]; then
    echo "Raspberry Pi/Debian系を検出しました"
    
    # PyQt5をシステムにインストール
    echo "PyQt5をインストール中..."
    sudo apt-get update
    sudo apt-get install -y python3-pyqt5 python3-venv
    
    # ChromeDriverをインストール（Qiita用）
    echo "ChromeDriverをインストール中..."
    sudo apt-get install -y chromium-chromedriver
    
    # 仮想環境を作成（システムパッケージを含める）
    echo "仮想環境を作成中..."
    python3 -m venv venv --system-site-packages
    
    # 仮想環境を有効化して残りをインストール
    echo "依存パッケージをインストール中..."
    source venv/bin/activate
    pip install -r requirements.txt
    
else
    echo "通常のPC環境を検出しました"
    
    # 仮想環境を作成
    echo "仮想環境を作成中..."
    python3 -m venv venv
    
    # 仮想環境を有効化してインストール
    echo "依存パッケージをインストール中..."
    source venv/bin/activate
    pip install PyQt5==5.15.9
    pip install -r requirements.txt
fi

# .envファイルのテンプレートを作成
if [ ! -f .env ]; then
    echo ".envファイルを作成中..."
    cat > .env << EOF
# Qiita
QIITA_TOKEN=your_qiita_bearer_token_here
ORGANIZATION_NAME=your_qiita_organization_name

# X (Twitter)
X_TOKEN=your_x_bearer_token_here
X_ACCOUNT=your_x_username

# Instagram
IG_TOKEN=your_instagram_access_token_here
IG_USER_ID=your_instagram_business_account_id

# Facebook
FB_TOKEN=your_facebook_access_token_here
FB_PAGE_ID=your_facebook_page_id
EOF
    echo ".envファイルを作成しました。各APIトークンを設定してください。"
fi

# アセットディレクトリを作成
if [ ! -d asset ]; then
    echo "assetディレクトリを作成中..."
    mkdir -p asset
    echo "asset/にSNSロゴ画像を配置してください。"
fi

echo ""
echo "=== セットアップ完了 ==="
echo "実行方法:"
echo "  source venv/bin/activate"
echo "  cd src"
echo "  python main.py"
echo ""
echo "※ .envファイルの設定を忘れずに！"