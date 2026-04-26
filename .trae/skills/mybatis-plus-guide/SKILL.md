---
name: "mybatis-plus-guide"
description: "MyBatis-Plus development guide covering CRUD operations, QueryWrapper, UpdateWrapper, Lambda usage, and chain programming. Invoke when user asks about MyBatis-Plus usage, wants to generate CRUD code, or needs help with database operations."
---

# MyBatis-Plus 开发指南

MyBatis-Plus 是一个强大的 MyBatis 增强工具，在不简化 CRUD 操作的同时，避免了编写繁琐的 SQL 语句。

## 核心组件

| 组件 | 说明 |
|------|------|
| BaseMapper | 通用 Mapper 接口，封装 CRUD 方法 |
| IService | 通用 Service 接口，封装业务层方法 |
| QueryWrapper | 查询条件构造器 |
| UpdateWrapper | 更新条件构造器 |
| LambdaQueryWrapper | 支持 Lambda 的查询构造器 |
| LambdaUpdateWrapper | 支持 Lambda 的更新构造器 |

---

## Service 层 (IService)

### 插入操作 (save)

```java
// 插入单条记录
boolean save(T entity);

// 批量插入
boolean saveBatch(Collection<T> entityList);

// 批量插入（指定批次大小）
boolean saveBatch(Collection<T> entityList, int batchSize);
```

```java
// 示例：插入单条记录
User user = new User();
user.setName("John Doe");
user.setEmail("john@example.com");
boolean result = userService.save(user);
// SQL: INSERT INTO user (name, email) VALUES ('John Doe', 'john@example.com')
```

```java
// 示例：批量插入，指定批次大小为 2
List<User> users = Arrays.asList(
    new User("Alice", "alice@example.com"),
    new User("Bob", "bob@example.com"),
    new User("Charlie", "charlie@example.com")
);
userService.saveBatch(users, 2);
// SQL: INSERT INTO user (name, email) VALUES ('Alice',...),('Bob',...) 
//      INSERT INTO user (name, email) VALUES ('Charlie',...)
```

### 插入或更新 (saveOrUpdate)

```java
// 存在则更新，不存在则插入
boolean saveOrUpdate(T entity);

// 批量修改插入
boolean saveOrUpdateBatch(Collection<T> entityList);
boolean saveOrUpdateBatch(Collection<T> entityList, int batchSize);
```

```java
// 示例：根据 ID 判断插入或更新
User user = new User();
user.setId(1);  // 如果 ID 存在则更新，不存在则插入
user.setName("John Doe");
userService.saveOrUpdate(user);
// 存在: UPDATE user SET name='John Doe' WHERE id=1
// 不存在: INSERT INTO user (id, name, ...) VALUES (1, 'John Doe', ...)
```

### 删除操作 (remove)

```java
// 根据条件删除
boolean remove(Wrapper<T> queryWrapper);

// 根据 ID 删除
boolean removeById(Serializable id);

// 根据 columnMap 条件删除
boolean removeByMap(Map<String, Object> columnMap);

// 批量删除
boolean removeByIds(Collection<? extends Serializable> idList);
```

```java
// 示例：根据条件删除
QueryWrapper<User> queryWrapper = new QueryWrapper<>();
queryWrapper.eq("name", "John Doe");
userService.remove(queryWrapper);
// SQL: DELETE FROM user WHERE name = 'John Doe'

// 示例：批量删除
userService.removeByIds(Arrays.asList(1, 2, 3));
// SQL: DELETE FROM user WHERE id IN (1, 2, 3)
```

### 更新操作 (update)

```java
// 根据 UpdateWrapper 更新
boolean update(Wrapper<T> updateWrapper);

// 根据实体和条件更新
boolean update(T updateEntity, Wrapper<T> whereWrapper);

// 根据 ID 更新
boolean updateById(T entity);

// 批量根据 ID 更新
boolean updateBatchById(Collection<T> entityList, int batchSize);
```

```java
// 示例：使用 UpdateWrapper 更新
UpdateWrapper<User> updateWrapper = new UpdateWrapper<>();
updateWrapper.eq("name", "John Doe").set("email", "new@email.com");
userService.update(updateWrapper);
// SQL: UPDATE user SET email='new@email.com' WHERE name='John Doe'

// 示例：根据 ID 批量更新
List<User> users = Arrays.asList(
    new User(1, null, "new.email1@example.com"),
    new User(2, null, "new.email2@example.com")
);
userService.updateBatchById(users, 2);
// SQL: UPDATE user SET email='new.email1@example.com' WHERE id=1
//      UPDATE user SET email='new.email2@example.com' WHERE id=2
```

### 查询操作 (get/list)

```java
// 根据 ID 查询
T getById(Serializable id);

// 查询单条记录（多个会抛异常）
T getOne(Wrapper<T> queryWrapper);

// 查询单条记录（可配置是否抛异常）
T getOne(Wrapper<T> queryWrapper, boolean throwEx);

// 查询全部
List<T> list();

// 条件查询
List<T> list(Wrapper<T> queryWrapper);

// 批量查询
Collection<T> listByIds(Collection<? extends Serializable> idList);
```

```java
// 示例：分页查询
IPage<User> page = new Page<>(1, 10);  // 第1页，每页10条
QueryWrapper<User> queryWrapper = new QueryWrapper<>();
queryWrapper.gt("age", 25);
IPage<User> userPage = userService.page(page, queryWrapper);
List<User> users = userPage.getRecords();
long total = userPage.getTotal();
// SQL: SELECT * FROM user WHERE age > 25 LIMIT 10 OFFSET 0
```

```java
// 示例：统计查询
int total = userService.count();
int count = userService.count(queryWrapper);
// SQL: SELECT COUNT(*) FROM user
// SQL: SELECT COUNT(*) FROM user WHERE age > 25
```

---

## Mapper 层 (BaseMapper)

### 插入操作

```java
// 插入一条记录
int insert(T entity);
```

```java
// 示例
User user = new User();
user.setName("John Doe");
user.setEmail("john@example.com");
int rows = userMapper.insert(user);
// SQL: INSERT INTO user (name, email) VALUES (?, ?)
```

### 删除操作

```java
// 根据条件删除
int delete(@Param(Constants.WRAPPER) Wrapper<T> wrapper);

// 根据 ID 批量删除
int deleteBatchIds(Collection<? extends Serializable> idList);

// 根据 ID 删除
int deleteById(Serializable id);

// 根据 columnMap 删除
int deleteByMap(Map<String, Object> columnMap);
```

```java
// 示例
userMapper.deleteById(1);  // SQL: DELETE FROM user WHERE id = 1
userMapper.deleteBatchIds(Arrays.asList(1, 2, 3));  
// SQL: DELETE FROM user WHERE id IN (1, 2, 3)
```

### 更新操作

```java
// 根据条件更新
int update(@Param(Constants.ENTITY) T updateEntity, @Param(Constants.WRAPPER) Wrapper<T> whereWrapper);

// 根据 ID 更新
int updateById(@Param(Constants.ENTITY) T entity);
```

### 查询操作

```java
// 根据 ID 查询
T selectById(Serializable id);

// 查询一条记录
T selectOne(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 批量查询
List<T> selectBatchIds(@Param(Constants.COLLECTION) Collection<? extends Serializable> idList);

// 条件查询
List<T> selectList(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 分页查询
IPage<T> selectPage(IPage<T> page, @Param(Constants.WRAPPER) Wrapper<T> queryWrapper);

// 统计查询
Integer selectCount(@Param(Constants.WRAPPER) Wrapper<T> queryWrapper);
```

---

## 条件构造器

### QueryWrapper 用法

```java
// 创建 QueryWrapper
QueryWrapper<User> queryWrapper = new QueryWrapper<>();

// 常用条件方法
queryWrapper.eq("name", "John");           // name = 'John'
queryWrapper.ne("name", "John");           // name <> 'John'
queryWrapper.gt("age", 18);                // age > 18
queryWrapper.ge("age", 18);                // age >= 18
queryWrapper.lt("age", 65);                // age < 65
queryWrapper.le("age", 65);                // age <= 65
queryWrapper.like("name", "John");          // name LIKE '%John%'
queryWrapper.likeLeft("name", "John");      // name LIKE '%John'
queryWrapper.likeRight("name", "John");    // name LIKE 'John%'
queryWrapper.in("id", 1, 2, 3);            // id IN (1,2,3)
queryWrapper.isNull("email");              // email IS NULL
queryWrapper.isNotNull("email");           // email IS NOT NULL
queryWrapper.between("age", 18, 65);       // age BETWEEN 18 AND 65
queryWrapper.notBetween("age", 18, 65);    // age NOT BETWEEN 18 AND 65
queryWrapper.inSql("id", "SELECT id FROM user WHERE age > 18");  // 子查询
queryWrapper.orderByAsc("age", "name");    // ORDER BY age ASC, name ASC
queryWrapper.orderByDesc("age", "name");   // ORDER BY age DESC, name DESC
queryWrapper.last("LIMIT 1");              // 拼接在 SQL 末尾

// 逻辑组合
queryWrapper.and(w -> w.eq("name", "John").or().eq("name", "Alice"));
// SQL: (name = 'John' OR name = 'Alice')

queryWrapper.or(w -> w.eq("name", "Bob").and(w2 -> w2.gt("age", 18)));
// SQL: name = 'Bob' OR (age > 18)
```

### UpdateWrapper 用法

```java
// 创建 UpdateWrapper
UpdateWrapper<User> updateWrapper = new UpdateWrapper<>();

// 设置更新字段
updateWrapper.set("name", "New Name");
updateWrapper.set("age", 30);
updateWrapper.setSql("name = 'Custom Expression'");  // 直接设置 SQL 片段

// 设置条件
updateWrapper.eq("id", 1);
// SQL: UPDATE user SET name='New Name', age=30 WHERE id = 1
```

### Lambda 用法（类型安全）

```java
// LambdaQueryWrapper
LambdaQueryWrapper<User> lambdaQuery = new QueryWrapper<User>()
    .lambda()
    .eq(User::getName, "John")
    .gt(User::getAge, 18)
    .like(User::getEmail, "@")
    .orderByDesc(User::getCreateTime);

// LambdaUpdateWrapper
LambdaUpdateWrapper<User> lambdaUpdate = new UpdateWrapper<User>()
    .lambda()
    .set(User::getEmail, "new@email.com")
    .eq(User::getId, 1);
```

### 使用 Wrappers 工具类

```java
import com.baomidou.mybatisplus.core.toolkit.Wrappers;

// 快速创建
List<User> users = userService.list(
    Wrappers.<User>lambdaQuery()
        .eq(User::getStatus, "active")
        .like(User::getName, "John")
        .orderByDesc(User::getCreateTime)
);

userService.update(
    Wrappers.<User>lambdaUpdate()
        .set(User::getEmail, "new@email.com")
        .eq(User::getId, 1)
);
```

---

## 链式编程 (Chain)

### 查询链

```java
// 普通链式查询
List<User> users = userService.query()
    .eq("name", "John")
    .like("email", "@")
    .list();

// Lambda 链式查询（推荐，类型安全）
User user = userService.lambdaQuery()
    .eq(User::getName, "John")
    .gt(User::getAge, 18)
    .one();
```

### 更新链

```java
// Lambda 链式更新
userService.lambdaUpdate()
    .set(User::getEmail, "new@email.com")
    .eq(User::getId, 1)
    .update();
```

---

## Db Kit（静态调用）

用于避免 Service 循环注入问题。

```java
import com.baomidou.mybatisplus.extension.toolkit.Db;

// 查询
User user = Db.getById(1L, User.class);
List<User> users = Db.listByIds(Arrays.asList(1L, 2L), User.class);
List<User> users = Db.list(Wrappers.lambdaQuery(User.class).eq(User::getStatus, "active"));

// 插入
Db.insert(new User("name", "email@example.com"));
Db.saveBatch(users);

// 更新
Db.updateById(user);
Db.update(null, Wrappers.lambdaUpdate(User.class).set(User::getAge, 30).eq(User::getId, 1));

// 删除
Db.removeById(1L);
Db.remove(Wrappers.lambdaQuery(User.class).eq(User::getStatus, "inactive"));
```

---

## ActiveRecord 模式

实体类继承 Model，直接调用 CRUD 方法。

```java
public class User extends Model<User> {
    private Long id;
    private String name;
    private Integer age;
    // getter/setter
}

// 使用
User user = new User();
user.setName("John");
user.setAge(30);
user.insert();                     // 插入

User queryUser = new User();
queryUser.setId(1L);
queryUser.selectById();            // 查询

queryUser.setName("Updated");
queryUser.updateById();            // 更新

queryUser.deleteById();           // 删除
```

---

## SimpleQuery 工具类

简化查询结果处理，支持 Stream 流操作。

```java
import com.baomidou.mybatisplus.core.toolkit.support.SimpleQuery;

// 查询并提取特定字段为 List
List<String> names = SimpleQuery.list(
    Wrappers.lambdaQuery(User.class).eq(User::getStatus, "active"),
    User::getName,
    user -> System.out.println("Processing: " + user.getName())
);

// 查询并封装为 Map（实体某个属性为 key）
Map<String, User> userMap = SimpleQuery.keyMap(
    Wrappers.lambdaQuery(User.class).eq(User::getStatus, "active"),
    User::getUsername
);

// 查询并封装为 Map（两个属性分别为 key 和 value）
Map<String, Integer> nameAgeMap = SimpleQuery.map(
    Wrappers.lambdaQuery(User.class).eq(User::getStatus, "active"),
    User::getUsername,
    User::getAge
);

// 按某个属性分组
Map<String, List<User>> grouped = SimpleQuery.group(
    Wrappers.lambdaQuery(User.class).eq(User::getStatus, "active"),
    User::getDepartment
);
```

---

## Mapper 层选装件

需要配合 Sql 注入器使用。

```java
// 强制更新某些字段（即使为 null）
int alwaysUpdateSomeColumnById(T entity);

// 批量插入（只插入非 null 字段）
int insertBatchSomeColumn(List<T> entityList);

// 逻辑删除并填充字段
int logicDeleteByIdWithFill(T entity);
```

---

## 分页查询配置

### 配置分页插件

```java
@Configuration
public class MybatisPlusConfig {
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor());
        return interceptor;
    }
}
```

### 使用分页

```java
// Service 层分页
IPage<User> page = new Page<>(1, 10);
IPage<User> result = userService.page(page, queryWrapper);

// Mapper 层分页
IPage<User> page = new Page<>(1, 10);
IPage<User> result = userMapper.selectPage(page, queryWrapper);

// 返回 Map 类型的分页
IPage<Map<String, Object>> pageMaps = userService.pageMaps(page);
```

---

## 常用注解

| 注解 | 说明 |
|------|------|
| @TableName | 指定表名 |
| @TableId | 指定主键（type = IdType.AUTO 自动增长） |
| @TableField | 指定字段映射 |
| @TableLogic | 标记逻辑删除字段 |

```java
@TableName("sys_user")
public class User {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("user_name")
    private String userName;
    
    @TableLogic
    private Integer deleted;
}
```

---

## 常见问题

### 1. 字段自动填充
```java
@Component
public class MyMetaObjectHandler implements MetaObjectHandler {
    @Override
    public void insertFill(MetaObject metaObject) {
        this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, LocalDateTime.now());
    }
    
    @Override
    public void updateFill(MetaObject metaObject) {
        this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
    }
}
```

### 2. 乐观锁
```java
@Version
private Integer version;
```

### 3. 枚举属性
```java
enum StatusEnum {
    NORMAL(0, "正常"),
    DISABLED(1, "禁用");
    
    @EnumValue
    private final int code;
    private final String desc;
}
```

---

## 快速参考

| 操作 | Mapper 方法 | Service 方法 |
|------|-------------|-------------|
| 插入 | insert() | save() |
| 删除 | deleteById() | removeById() |
| 更新 | updateById() | updateById() |
| 查询单条 | selectById() | getById() |
| 查询列表 | selectList() | list() |
| 分页查询 | selectPage() | page() |
| 统计 | selectCount() | count() |
