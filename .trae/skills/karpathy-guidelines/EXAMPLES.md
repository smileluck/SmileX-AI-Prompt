# Examples - 代码示例

真实世界的代码示例，演示四大原则。每个示例展示 LLM 通常做错什么以及如何修复。

---

## 1. Think Before Coding

### 示例 1: 隐藏假设

**用户请求：** "添加一个导出用户数据的功能"

**❌ LLM 错误做法（错误假设）**
```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()
    
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    
    return f"Exported {len(users)} users"
```

**问题：**
- 假设应该导出所有用户（分页？隐私？）
- 假设文件位置而不询问
- 假设包含哪些字段
- 假设 CSV 字段名而不检查实际数据结构

**✅ 正确做法（显式假设）**
```
在实现之前，我需要澄清：
1. **范围**：导出所有用户还是过滤子集？（隐私影响）
2. **格式**：你说的是"导出"——你是指：
   - 下载文件在浏览器？
   - 后台任务带邮件通知？
   - 返回数据的 API 端点？
3. **字段**：哪些用户字段？（有些可能是敏感的）
4. **数量**：通常有多少用户？（影响方法选择）

最简单的方法：添加一个返回分页 JSON 的 API 端点。
文件导出需要更多信息。
你偏好哪种方式？
```

---

### 示例 2: 多重解释

**用户请求：** "让搜索更快"

**❌ LLM 错误做法（静默选择）**
```python
# 添加了缓存、数据库索引和异步处理
# 而不询问哪种"更快"更重要
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # ... 200 行优化代码
```

**✅ 正确做法**
```
"让搜索更快"可能意味着：
1. **更快的响应时间** (< 100ms 而不是 500ms)
   - 添加数据库索引
   - 缓存频繁查询
   - 预估工作量：2 小时

2. **处理更多并发搜索** (吞吐量)
   - 添加 async/await
   - 连接池
   - 预估工作量：4 小时

3. **更快的感知速度** (UX)
   - 立即显示部分结果
   - 渐进式加载
   - 预估工作量：3 小时

当前搜索典型查询耗时约 500ms。
你的使用场景最看重哪个方面？
```

---

## 2. Simplicity First

### 示例 1: 过度抽象

**用户请求：** "添加一个计算折扣的函数"

**❌ LLM 错误做法（过度工程）**
```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol, Union
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)

# 使用需要 30+ 行设置代码来做一个简单计算
```

**✅ 正确做法（简单）**
```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)

# Usage
discount = calculate_discount(100.0, 10.0)  # $10 off
```

**何时添加复杂性：** 只有在真正需要多种折扣类型时。如果需求后来出现，届时再重构。

---

### 示例 2: 投机性功能

**用户请求：** "保存用户偏好到数据库"

**❌ LLM 错误做法（不必要功能）**
```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()
    
    def save(self, user_id: int, prefs: dict, 
             merge: bool = True, 
             validate: bool = True,
             notify: bool = False) -> bool:
        """Save preferences with optional merging, validation, and notifications."""
        
        if validate:
            errors = self.validator.validate(prefs)
            if errors:
                raise ValidationError(errors)
        
        existing = self.get(user_id) if merge else {}
        
        if merge:
            existing.update(prefs)
            prefs = existing
        
        self.db.execute(
            "UPDATE users SET preferences = ? WHERE id = ?",
            (json.dumps(prefs), user_id)
        )
        
        if self.cache:
            self.cache.set(f"prefs:{user_id}", prefs)
        
        if notify:
            self.notify_preference_change(user_id, prefs)
        
        return True
    
    def notify_preference_change(self, user_id: int, prefs: dict):
        # 又一个没人要求的功能，30 行代码
        pass
```

**✅ 正确做法（只做要求的）**
```python
def save_preferences(db, user_id: int, preferences: dict):
    """Save user preferences to database."""
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

**如果需要稍后添加：** 缓存（当性能重要时）、验证（当有坏数据出现时）、合并（当需求出现时）。

---

## 3. Surgical Changes

### 示例 1: 顺便重构

**用户请求：** "修复空邮箱导致验证器崩溃的 bug"

**❌ LLM 错误做法（改动太多）**
```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     
+     # Validate email
+     if not email:
          raise ValueError("Email required")
-     
-     # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
      
-     # Check username
-     if not user_data.get('username'):
+     # Validate username
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
+     if not username.isalnum():
+         raise ValueError("Username must be alphanumeric")
      
      return True
```

**问题：**
- "改进了"超出 bug 修复范围的邮件验证
- 添加了没人要求的用户名验证
- 改了注释
- 添加了文档字符串

**✅ 正确做法（精准手术）**
```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      
      # Check username
      if not user_data.get('username'):
          raise ValueError("Username required")
      
      return True
```

**只改了：** 修复空邮件处理的具体代码行。

---

### 示例 2: 风格漂移

**用户请求：** "给上传函数添加日志"

**❌ LLM 错误做法（重格式化一切）**
```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
+     logger.info(f"Uploading {file_path} to {destination}")
+     
      try:
-         with open(file_path, 'rb') as f:
-             data = f.read()
-         
-         response = requests.post(destination, files={'file': data})
-         
-         if response.status_code == 200:
-             return True
-         else:
-             return False
+         with open(file_path, "rb") as f:
+             data = f.read()
+         response = requests.post(destination, files={"file": data})
+         success = response.status_code == 200
+         
+         if success:
+             logger.info(f"Upload successful: {file_path}")
+         else:
+             logger.error(f"Upload failed: {file_path}, status={response.status_code}")
+         
+         return success
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f"Upload error for {file_path}: {e}")
          return False
```

**问题：**
- 改了引号风格（'' 到 ""）
- 添加了没人要求的类型提示
- 添加了文档字符串
- 重格式化了空白
- 改了布尔返回逻辑

**✅ 正确做法（匹配现有风格）**
```diff
+ import logging
+ 
+ logger = logging.getLogger(__name__)
+ 
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
              data = f.read()
          
          response = requests.post(destination, files={'file': data})
          
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

**匹配了：** 单引号、无类型提示、现有布尔模式、间距风格。

---

## 4. Goal-Driven Execution

### 示例 1: 模糊 vs 可验证

**用户请求：** "修复认证系统"

**❌ LLM 错误做法（模糊方法）**
```
我会修复认证系统：
1. 审查代码
2. 识别问题
3. 做改进
4. 测试更改
[不明确成功标准就进行更改]
```

**✅ 正确做法（可验证目标）**
```
要"修复认证"，我需要定义成功标准。
我们要解决什么具体问题？

如果问题是"密码更改后用户仍然保持登录"：
计划：
1. 写测试：更改密码 → 验证旧会话被使无效
   验证：测试失败（复现 bug）
2. 实现：密码更改时使会话失效
   验证：测试通过
3. 检查边界情况：多个活动会话、并发更改
   验证：附加测试通过
4. 验证无回归：现有 auth 测试仍然通过
   验证：完整测试套件绿色

当前 auth 测试覆盖率：[显示覆盖率]
你看到的具体 auth 问题是什么？
```

---

### 示例 2: 带验证的多步骤

**用户请求：** "给 API 添加速率限制"

**❌ LLM 错误做法（一次性全部）**
```python
# 用 Redis、多种策略、配置系统和监控
# 在一个 300 行的 commit 中实现完整速率限制
# 没有明确的验证步骤
```

**✅ 正确做法（增量验证）**
```
速率限制计划：
1. 添加基本内存速率限制（单个端点）
   验证：
   - 测试：100 请求 → 前 10 个成功，剩余得到 429
   - 手动：curl 端点 11 次，看到速率限制错误

2. 提取到中间件（应用到所有端点）
   验证：
   - 测试：速率限制应用于 /users 和 /posts
   - 现有端点测试仍然通过

3. 添加 Redis 后端（用于多服务器）
   验证：
   - 测试：速率限制在应用重启后保持
   - 测试：两个应用实例共享速率限制计数器

4. 添加配置（每个端点的速率）
   验证：
   - 测试：/search 允许 10/min，/users 允许 100/min
   - 配置文件正确解析

每个步骤独立可验证和可部署。
从步骤 1 开始？
```

---

### 示例 3: 测试优先验证

**用户请求：** "当有重复分数时排序坏了"

**❌ LLM 错误做法（不复现就修复）**
```python
# 立即更改排序逻辑而不确认 bug
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))
```

**✅ 正确做法（先复现）**
```python
# 1. 首先，写一个复现问题的测试
def test_sort_with_duplicate_scores():
    """Test sorting when multiple items have same score."""
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    
    result = sort_scores(scores)
    
    # Bug：重复项的顺序是不确定的
    # 运行这个测试多次，它应该是一致的
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90

# 验证：运行测试 10 次 → 因顺序不一致而失败

# 2. 现在用稳定排序修复
def sort_scores(scores):
    """Sort by score descending, then name ascending for ties."""
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# 验证：测试持续通过
```

---

## 反模式总结

| 原则 | 反模式 | 修复 |
|------|--------|------|
| Think Before Coding | 静默假设文件格式、字段、范围 | 显式列出假设，要求澄清 |
| Simplicity First | 单个折扣计算用策略模式 | 一个函数直到真正需要复杂性 |
| Surgical Changes | 修复 bug 时重格式化引号、添加类型提示 | 只改修复报告问题的代码行 |
| Goal-Driven | "我会审查和改进代码" | "为 bug X 写测试 → 让它通过 → 验证无回归" |

---

## 关键洞察

"过度复杂"的示例不是明显错误的——它们遵循设计模式和最佳实践。问题是**时机**：在需要之前添加复杂性，这会：

- 使代码更难理解
- 引入更多 bug
- 需要更长时间实现
- 更难测试

"简单"版本：
- 更容易理解
- 更快实现
- 更容易测试
- 以后需要时可以重构

**好代码是简单解决今天问题的代码，而不是 premature 地解决明天问题的代码。**
