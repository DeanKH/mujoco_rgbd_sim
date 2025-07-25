# MuJoCo RGBD Simulation

MuJoCo を使用して RGBD カメラシミュレーションを行う Python ライブラリです。仮想シーンに複数のカメラを配置し、RGB 画像と深度画像を取得できます。

## 特徴

- 🎥 複数の RGBD カメラの配置とシミュレーション
- 📐 カメラの内部パラメータ（intrinsic matrix）の自動計算
- 🎨 RGB 画像と深度画像の同時取得
- 📊 深度データから 3D 点群（XYZ 形式）への変換
- 🔧 シンプルなシーンビルダー API
- 📦 MuJoCo の物理シミュレーション機能を活用

## インストール

このプロジェクトは`uv`パッケージマネージャーを使用しています。

```bash
# uvのインストール（まだインストールしていない場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール
uv sync

# 開発モードでのインストール
uv pip install -e .
```

## クイックスタート

```python
import mujoco_rgbd_sim.mujoco_scene_builder as sb
import mujoco_rgbd_sim.mujoco_sim as ms
import cv2

# カメラの設定
camera = sb.Camera(
    name="main_camera",
    position=(0, 0, 1.5),
    fovy=60.0,
    camera_width=640,
    camera_height=480,
)

# オブジェクトの作成
box = sb.Box(
    name="red_box",
    size=(0.1, 0.1, 0.1),
    position=(0, 0, 0.05),
    color=(0.8, 0.2, 0.2, 1.0),
)

# シーンの構築
xml_str = (
    sb.MujocoSceneBuilder()
    .set_scene_template_file("example/empty_scene.xml")
    .add_camera(camera)
    .add_object(box)
    .build()
)

# シミュレーションの実行
sim = ms.MujocoSimulation()
sim.setup(xml_str)

# 画像の取得
rgb_image, depth_image = sim.capture_image(camera)

# 画像の表示
cv2.imshow("RGB", rgb_image)
cv2.imshow("Depth", depth_image)
cv2.waitKey(0)
```

## API リファレンス

### MujocoSceneBuilder

シーンを構築するためのビルダークラス。

```python
builder = sb.MujocoSceneBuilder()
builder.set_scene_template_file("template.xml")  # テンプレートファイルを設定
builder.add_camera(camera)                       # カメラを追加
builder.add_object(object)                       # オブジェクトを追加
xml_str = builder.build()                        # XMLを生成
```

### Camera

カメラオブジェクトを定義するクラス。

```python
camera = sb.Camera(
    name="camera_name",
    position=(x, y, z),              # カメラ位置
    fovy=60.0,                       # 垂直視野角（度）
    xyaxes=(1, 0, 0, 0, 1, 0),      # カメラの向き
    camera_width=640,                # 画像幅
    camera_height=480,               # 画像高さ
)

# カメラ内部パラメータの取得
intrinsic_matrix = camera.get_camera_matrix()
```

### オブジェクトクラス

#### Box

```python
box = sb.Box(
    name="box1",
    size=(width, height, depth),     # サイズ
    position=(x, y, z),              # 位置
    euler=(rx, ry, rz),              # 回転（オイラー角）
    color=(r, g, b, a),              # 色（RGBA）
)
```

#### Cylinder

```python
cylinder = sb.Cylinder(
    name="cylinder1",
    radius=0.05,                     # 半径
    height=0.2,                      # 高さ
    position=(x, y, z),              # 位置
    euler=(rx, ry, rz),              # 回転
    color=(r, g, b, a),              # 色
)
```

### MujocoSimulation

シミュレーションを実行するクラス。

```python
sim = ms.MujocoSimulation()
sim.setup(xml_string)                            # XMLからシミュレーションを初期化
rgb, depth = sim.capture_image(camera)           # RGB・深度画像を取得
```

## 完全な使用例

`example/simple_camera.py`に完全な使用例があります：

```bash
# サンプルの実行
uv run python example/simple_camera.py
```

このサンプルでは：

1. 天井カメラと手持ちカメラの 2 つを配置
2. 赤い箱をシーンに追加
3. 各カメラから RGB・深度画像を取得
4. 深度データを 3D 点群（XYZ 形式）に変換して保存

## 出力フォーマット

### XYZ 点群フォーマット

深度画像から生成される点群データは、以下の形式で保存されます：

```
x1 y1 z1
x2 y2 z2
...
```

各行が 1 つの 3D 点を表し、単位はメートルです。

## 必要条件

- Python >= 3.8
- MuJoCo >= 3.0.0
- OpenCV >= 4.8.0
- NumPy >= 1.24.0
- matplotlib >= 3.7.0

## プロジェクト構造

```
mujoco_rgbd_sim/
├── mujoco_rgbd_sim/
│   ├── __init__.py
│   ├── mujoco_camera.py        # カメラクラスと内部パラメータ計算
│   ├── mujoco_scene_builder.py # シーンビルダーとオブジェクトクラス
│   └── mujoco_sim.py           # シミュレーション実行
├── example/
│   ├── empty_scene.xml         # シーンテンプレート
│   └── simple_camera.py        # 使用例
├── pyproject.toml              # プロジェクト設定
└── README.md                   # このファイル
```

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。
