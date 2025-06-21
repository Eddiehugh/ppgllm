"""
简化的命令行测试工具
用于快速验证Agent系统功能
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.agent_manager import AgentManager

async def test_simple_cli():
    """简化的命令行测试工具"""
    print("🚀 隐私政策智能生成系统 - 简易测试工具")
    print("----------------------------------------")

    # 初始化Agent管理器
    manager = AgentManager()

    # 获取可用Agent列表 - 直接使用异步调用
    agents = await manager.get_available_agents()
    print(f"📋 可用Agent列表:")
    for i, agent in enumerate(agents, 1):
        print(f"  {i}. {agent['name']} ({agent['type']})")

    # 预设的测试消息
    test_messages = {
        "privacy_policy_generator": "为一个社交应用生成简单的隐私政策",
        "compliance_checker": "检查这个隐私政策是否合规：我们收集用户信息用于提供服务",
        "readability_checker": "评估这段文字的可读性：本隐私政策阐述了我们如何收集您的信息"
    }

    while True:
        print("\n----------------------------------------")
        print("请选择要测试的Agent:")
        print("1. 隐私政策生成专家")
        print("2. 合规性检测专家")
        print("3. 可读性检测专家")
        print("4. 自动选择Agent")
        print("0. 退出")

        choice = input("\n请输入选项编号: ")

        if choice == "0":
            print("👋 测试结束，再见！")
            break

        elif choice == "1":
            agent_type = "privacy_policy_generator"
            message = test_messages[agent_type]

        elif choice == "2":
            agent_type = "compliance_checker"
            message = test_messages[agent_type]

        elif choice == "3":
            agent_type = "readability_checker"
            message = test_messages[agent_type]

        elif choice == "4":
            # 自动选择Agent
            print("\n请选择测试消息:")
            print("1. 生成隐私政策")
            print("2. 检查合规性")
            print("3. 评估可读性")

            msg_choice = input("请选择: ")
            if msg_choice == "1":
                message = "请帮我生成一个隐私政策"
            elif msg_choice == "2":
                message = "检查这个隐私政策是否合规"
            elif msg_choice == "3":
                message = "这个文档的可读性如何？"
            else:
                print("❌ 无效选择")
                continue

            print(f"\n🔄 测试自动选择Agent...")
            print(f"📝 测试消息: {message}")

            selected_agent = manager.select_agent_by_intent(message)
            print(f"🤖 自动选择的Agent: {selected_agent}")

            result = await manager.auto_process_request(message=message)

            if result["success"]:
                print("✅ 测试成功!")
                if result.get('response'):
                    print(f"📝 回复摘要: {result.get('response')}...")
                else:
                    print("📝 无回复内容")
            else:
                print(f"❌ 测试失败: {result.get('error', '未知错误')}")

            continue

        else:
            print("❌ 无效的选项，请重新选择")
            continue

        # 执行测试
        print(f"\n🔄 测试Agent: {agent_type}")
        print(f"📝 测试消息: {message}")

        result = await manager.process_request(
            agent_type=agent_type,
            message=message,
            context=None
        )

        if result["success"]:
            print("✅ 测试成功!")
            if result.get('response'):
                print(f"📝 回复摘要: {result.get('response')}...")
            else:
                print("📝 无回复内容")
        else:
            print(f"❌ 测试失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    print("🚀 启动简易测试工具...")

    try:
        asyncio.run(test_simple_cli())
    except KeyboardInterrupt:
        print("\n👋 程序已中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
