# How to Add Variables in GitLab CI/CD Settings - Step by Step

## 🎯 Exact Steps to Add Variables

### Step 1: Navigate to Variables Page

1. Open your GitLab project in a web browser
2. Look at the **left sidebar menu**
3. Click on **Settings** (usually near the bottom, has a gear icon ⚙️)
4. In the Settings submenu, click **CI/CD** (or scroll down to find it)
5. **Expand** the **Variables** section (click the arrow or "Expand" button)

You should now see:
- A list of existing variables (if any)
- A blue button that says **"Add variable"** or **"Add new variable"**

### Step 2: Click "Add variable" Button

Click the **"Add variable"** button.

A form will appear with these fields:

```
┌─────────────────────────────────────────┐
│ Key: [________________]                 │
│ Value: [________________]               │
│ Type: Variable ▼                       │
│ Environment scope: * (All environments)│
│ Flags:                                  │
│   ☐ Protect variable                   │
│   ☐ Mask variable                      │
│   ☐ Expand variable reference          │
│                                         │
│ [Cancel]  [Add variable]                │
└─────────────────────────────────────────┘
```

### Step 3: Fill in the Form for Each Variable

Let's add your first variable as an example:

#### Example 1: Adding `USE_CUSTOM_GATEWAY`

1. **Key field**: Type exactly: `USE_CUSTOM_GATEWAY`
   - Must match exactly (case-sensitive)
   - No spaces before/after

2. **Value field**: Type: `true`
   - This is not sensitive, so no masking needed

3. **Type**: Leave as **Variable** (default)

4. **Environment scope**: Leave as **All environments** (default)

5. **Flags** (checkboxes):
   - ☑️ **Protect variable**: Check this box
   - ☐ **Mask variable**: Leave unchecked (not sensitive)
   - ☑️ **Expand variable reference**: Check this box

6. Click **"Add variable"** button at the bottom

✅ Done! You've added your first variable.

#### Example 2: Adding `CUSTOM_GATEWAY_API_KEY` (Sensitive)

1. **Key**: `CUSTOM_GATEWAY_API_KEY`

2. **Value**: Paste your actual API key here
   - Example: `abc123xyz456...` (your real key)

3. **Type**: **Variable** (default)

4. **Environment scope**: **All environments** (default)

5. **Flags**:
   - ☑️ **Protect variable**: ✅ CHECK THIS
   - ☑️ **Mask variable**: ✅ CHECK THIS (important for secrets!)
   - ☑️ **Expand variable reference**: ✅ CHECK THIS

6. Click **"Add variable"**

⚠️ **Important**: After you save a masked variable, you won't be able to see its value again in the UI (it shows as `****`). This is for security.

#### Example 3: Adding `GENAI_PASSWORD` (Sensitive)

Same as Example 2:
- **Key**: `GENAI_PASSWORD`
- **Value**: Your actual password
- **Protect**: ✅ Checked
- **Mask**: ✅ Checked
- **Expand**: ✅ Checked

### Step 4: Repeat for All Variables

Add each variable one by one using the same process:

**For Custom Gateway Setup:**

| Variable Name | Value | Protect? | Mask? | Expand? |
|--------------|-------|-----------|-------|---------|
| `USE_CUSTOM_GATEWAY` | `true` | ✅ | ❌ | ✅ |
| `CUSTOM_GATEWAY_API_KEY` | Your API key | ✅ | ✅ | ✅ |
| `CUSTOM_GATEWAY_BASE_URL` | Your URL | ✅ | ❌ | ✅ |
| `GENAI_USERNAME` | Your username | ✅ | ✅ | ✅ |
| `GENAI_PASSWORD` | Your password | ✅ | ✅ | ✅ |
| `CUSTOM_MODEL` | `Llama-3.3-70B-Instruct` | ✅ | ❌ | ✅ |

**For OpenAI Setup:**

| Variable Name | Value | Protect? | Mask? | Expand? |
|--------------|-------|-----------|-------|---------|
| `OPENAI_API_KEY` | `sk-...` | ✅ | ✅ | ✅ |

**Optional Variables:**

| Variable Name | Value | Protect? | Mask? | Expand? |
|--------------|-------|-----------|-------|---------|
| `USER_SIMULATOR_MODEL` | `gpt-4o-mini` | ❌ | ❌ | ✅ |
| `JUDGE_MODEL` | `gpt-4o` | ❌ | ❌ | ✅ |
| `LANGWATCH_API_KEY` | Your key | ✅ | ✅ | ✅ |
| `LANGWATCH_ENDPOINT` | `https://app.langwatch.ai` | ❌ | ❌ | ✅ |

### Step 5: Verify Variables Are Added

After adding all variables, you should see them listed in the Variables section:

```
Variables
┌─────────────────────────────────────────────┐
│ Key                        Environment      │
│ USE_CUSTOM_GATEWAY        *                │
│ CUSTOM_GATEWAY_API_KEY    *        [Edit]   │
│ CUSTOM_GATEWAY_BASE_URL   *        [Edit]   │
│ ...                                        │
└─────────────────────────────────────────────┘
```

## 🎨 Visual Guide to Form Fields

When you click "Add variable", here's what each field means:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Key:                                           │
│  ┌─────────────────────────────────────────┐   │
│  │ USE_CUSTOM_GATEWAY                      │   │ ← Type variable name here
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Value:                                         │
│  ┌─────────────────────────────────────────┐   │
│  │ true                                     │   │ ← Type the value here
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Type: [Variable ▼]                            │ ← Usually leave as "Variable"
│                                                 │
│  Environment scope: [* (All environments) ▼]   │ ← Usually leave as "*"
│                                                 │
│  Flags:                                         │
│  ☑ Protect variable                            │ ← Check for sensitive data
│  ☑ Mask variable                               │ ← Check for secrets (API keys)
│  ☑ Expand variable reference                   │ ← Usually check this
│                                                 │
│              [Cancel]  [Add variable]           │ ← Click to save
│                                                 │
└─────────────────────────────────────────────────┘
```

## ❓ Common Questions

**Q: I don't see "Add variable" button**
- Make sure you're in **Settings → CI/CD → Variables**
- Make sure you have permission to edit project settings
- Try refreshing the page

**Q: What if I make a mistake?**
- Click **Edit** (pencil icon) next to the variable
- Change the value
- Click **Update variable**

**Q: Can I see the value after masking?**
- No, masked variables show as `****` for security
- You'll need to re-enter if you forget

**Q: What does "Protect variable" do?**
- Makes variable only available on protected branches
- Prevents accidental use on feature branches
- Good for production secrets

**Q: What does "Mask variable" do?**
- Hides the value in CI/CD job logs
- Prevents secrets from appearing in pipeline output
- Always use this for API keys and passwords

**Q: What does "Expand variable reference" do?**
- Allows using variables inside other variables
- Example: `BASE_URL=https://${DOMAIN}/api`
- Usually safe to enable

## ✅ Checklist

After adding all variables, verify:

- [ ] All variables are listed in the Variables page
- [ ] Sensitive variables show `****` (masked)
- [ ] Protected variables have a lock icon 🔒
- [ ] Variable names match exactly what your code expects
- [ ] No typos in variable names (case-sensitive!)

## 🚀 Next Step

Once all variables are added:
1. Go to **CI/CD → Pipelines**
2. Click **Run pipeline**
3. Select your branch
4. Watch it run!

Your tests will automatically have access to all these variables through `os.getenv()` calls in your code.

