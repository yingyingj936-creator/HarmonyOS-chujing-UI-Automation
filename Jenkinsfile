pipeline {
    agent any

    environment {
        // 显式指定 HDC 路径，防止 Jenkins 找不到命令
        HDC_EXE = "D:\\Hdc\\toolchains-windows-x64-5.1.0.56-Beta1\\toolchains\\hdc.exe"
        // 你的无线设备 IP 和端口
        TARGET_IP = "172.16.130.172:5555"
        // 虚拟环境中的 Python 路径 (Win11 虚拟环境通常在 Scripts 下)
        VENV_PYTHON = "${WORKSPACE}\\.venv\\Scripts\\python.exe"
        // Allure 原始数据目录
        ALLURE_RESULTS = "reports"
    }

    stages {
        stage('环境初始化') {
            steps {
                // 强制清理旧进程，防止之前的测试进程挂死导致本次无法连接手机
                bat """
                    echo "正在清理旧的测试进程和 HDC 服务..."
                    taskkill /F /IM hdc.exe /T >nul 2>&1
                    "${HDC_EXE}" start
                """
            }
        }

        stage('无线设备连接') {
            steps {
                bat """
                    echo "正在连接 HarmonyOS 设备: ${TARGET_IP}"
                    "${HDC_EXE}" tconn ${TARGET_IP}
                    timeout /t 5
                    "${HDC_EXE}" list targets
                """
            }
        }

        stage('准备测试环境') {
            steps {
                // 确保依赖库是最新的
                bat """
                    if not exist ".venv" (
                        echo "[ERROR] 未在根目录找到 .venv 环境，请检查部署路径"
                        exit 1
                    )
                    "${VENV_PYTHON}" -m pip install --upgrade pip
                    "${VENV_PYTHON}" -m pip install -r requirements.txt
                """
            }
        }

        stage('执行 UI 自动化') {
            steps {
                // 运行 pytest
                // --clean-alluredir 确保每次报告都是全新的，不会包含上一次运行的干扰数据
                bat """
                    "${VENV_PYTHON}" -m pytest tests/ --alluredir=${ALLURE_RESULTS} --clean-alluredir
                """
            }
        }
    }

    post {
        always {
            // 生成 Allure 报告 (Jenkins 会自动把 reports 下的 json 转为可视化图表)
            allure includeProperties: false, jdk: '', results: [[path: "${ALLURE_RESULTS}"]]
            
            // 结束后断开连接，释放资源
            bat "\"${HDC_EXE}\" tdisconn ${TARGET_IP}"
        }
    }
}
