"""
系统测试脚本
用于验证各个Agent的功能
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents import AgentManager


async def test_agents():
    """测试所有Agent的基本功能"""
    print("🧪 开始测试Agent系统...")
    
    try:
        # 初始化Agent管理器
        manager = AgentManager()
        print("✅ Agent管理器初始化成功")
        
        # 获取Agent列表
        agents = manager.get_available_agents()
        print(f"📋 可用Agent数量: {len(agents)}")
        for agent in agents:
            print(f"   - {agent['name']} ({agent['type']}): {agent['status']}")
        
        # 测试隐私政策生成Agent
        print("\n🔧 测试隐私政策生成Agent...")
        generator = manager.get_agent("privacy_policy_generator")
        app_info = {
            "name": "测试应用",
            "type": "社交应用",
            "data_types": ["用户信息", "设备信息"],
            "regions": ["中国"]
        }
        
        result = await generator.generate_privacy_policy(app_info, "简单测试")
        if result["success"]:
            print("✅ 隐私政策生成测试通过")
            print(f"   回复长度: {len(result.get('response', ''))}")
        else:
            print(f"❌ 隐私政策生成测试失败: {result.get('error', 'Unknown error')}")
        
        # 测试合规性检测Agent
        print("\n🔍 测试合规性检测Agent...")
        compliance_checker = manager.get_agent("compliance_checker")
        test_policy = "这是一个测试隐私政策内容，用于检测合规性。"
        
        result = await compliance_checker.quick_compliance_check(test_policy)
        if result["success"]:
            print("✅ 合规性检测测试通过")
            print(f"   回复长度: {len(result.get('response', ''))}")
        else:
            print(f"❌ 合规性检测测试失败: {result.get('error', 'Unknown error')}")
        
        # 测试可读性检测Agent
        print("\n📖 测试可读性检测Agent...")
        readability_checker = manager.get_agent("readability_checker")
        
        result = await readability_checker.quick_readability_check(test_policy)
        if result["success"]:
            print("✅ 可读性检测测试通过")
            print(f"   回复长度: {len(result.get('response', ''))}")
        else:
            print(f"❌ 可读性检测测试失败: {result.get('error', 'Unknown error')}")
        
        # 测试自动Agent选择
        print("\n🤖 测试自动Agent选择...")
        test_messages = [
            "请帮我生成一个隐私政策",
            "检查这个隐私政策是否合规",
            "这个文档的可读性如何？"
        ]
        
        for message in test_messages:
            selected_agent = manager.select_agent_by_intent(message)
            print(f"   '{message}' -> {selected_agent}")
        
        print("\n🎉 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


async def test_api_models():
    """测试API数据模型"""
    print("\n📊 测试API数据模型...")
    
    try:
        from src.api.models import ChatRequest, PrivacyPolicyGenerateRequest
        
        # 测试ChatRequest
        chat_req = ChatRequest(
            agent_type="privacy_policy_generator",
            message="测试消息",
            context={"test": "data"}
        )
        print("✅ ChatRequest模型测试通过")
        
        # 测试PrivacyPolicyGenerateRequest
        gen_req = PrivacyPolicyGenerateRequest(
            app_name="测试应用",
            app_type="工具应用",
            data_types=["用户信息"],
            regions=["中国"]
        )
        print("✅ PrivacyPolicyGenerateRequest模型测试通过")
        
    except Exception as e:
        print(f"❌ API模型测试失败: {str(e)}")


if __name__ == "__main__":
    print("🚀 启动系统测试...")
    
    # 运行异步测试
    asyncio.run(test_agents())
    
    # 运行同步测试
    asyncio.run(test_api_models())
    
    print("\n✨ 测试完成！如果所有测试都通过，系统应该可以正常运行。")
    print("💡 提示：请确保已正确配置GLM API密钥后再启动完整系统。")