# streamlit-win5



## 環境構築

### 初期設定

```bash
# 仮想環境の作成
python3.13 -m venv ./develop/venv

# 仮想環境を有効化
source ./develop/venv/bin/activate  # Linux/MacOS

pip install streamlit

# 依存関係の保存
pip freeze > ./app/requirements.txt

# ローカル環境での実行
uvicorn app.main:app --reload


```

### ２回目以降

```bash
# 仮想環境を有効化
source ./develop/venv/bin/activate  # Linux/MacOS

# 依存関係のインストール
pip install -r ./app/requirements.txt
```

### アプリケーションの起動

```bash
streamlit run app/win5_app.py
```