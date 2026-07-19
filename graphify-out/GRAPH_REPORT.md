# Graph Report - .  (2026-07-19)

## Corpus Check
- 109 files · ~78,772 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 395 nodes · 442 edges · 34 communities (22 shown, 12 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Cursor Review Agents|Cursor Review Agents]]
- [[_COMMUNITY_Template Cursor Settings|Template Cursor Settings]]
- [[_COMMUNITY_Sample Cursor Settings|Sample Cursor Settings]]
- [[_COMMUNITY_Agent Skills Workflow|Agent Skills Workflow]]
- [[_COMMUNITY_Sample Project Docs|Sample Project Docs]]
- [[_COMMUNITY_Template Docs References|Template Docs References]]
- [[_COMMUNITY_Coverage Report Status|Coverage Report Status]]
- [[_COMMUNITY_Cookiecutter Generation|Cookiecutter Generation]]
- [[_COMMUNITY_Template Main Tests|Template Main Tests]]
- [[_COMMUNITY_Template CI Tooling|Template CI Tooling]]
- [[_COMMUNITY_Cookiecutter Variables|Cookiecutter Variables]]
- [[_COMMUNITY_App Entrypoint Coverage|App Entrypoint Coverage]]
- [[_COMMUNITY_Dependency Manager Tests|Dependency Manager Tests]]
- [[_COMMUNITY_Sample Main Tests|Sample Main Tests]]
- [[_COMMUNITY_Agent Orchestration|Agent Orchestration]]
- [[_COMMUNITY_Coverage HTML UI|Coverage HTML UI]]
- [[_COMMUNITY_Coverage Favicon Brand|Coverage Favicon Brand]]
- [[_COMMUNITY_API Context Skills|API Context Skills]]
- [[_COMMUNITY_Coverage Keyboard Icon|Coverage Keyboard Icon]]
- [[_COMMUNITY_RTK Rewrite Hook|RTK Rewrite Hook]]
- [[_COMMUNITY_Cursor Hooks Config|Cursor Hooks Config]]
- [[_COMMUNITY_RTK Install Script|RTK Install Script]]
- [[_COMMUNITY_Skills Sync Script|Skills Sync Script]]
- [[_COMMUNITY_Template Package Init|Template Package Init]]
- [[_COMMUNITY_Template Tests Init|Template Tests Init]]
- [[_COMMUNITY_Root Cursor Settings|Root Cursor Settings]]
- [[_COMMUNITY_Post-Gen Hook|Post-Gen Hook]]
- [[_COMMUNITY_Pre-Gen Hook|Pre-Gen Hook]]
- [[_COMMUNITY_Sample Package Init|Sample Package Init]]
- [[_COMMUNITY_Sample Tests Init|Sample Tests Init]]
- [[_COMMUNITY_Accessibility Checklist|Accessibility Checklist]]
- [[_COMMUNITY_Performance Checklist|Performance Checklist]]
- [[_COMMUNITY_Idea Refine Script|Idea Refine Script]]

## God Nodes (most connected - your core abstractions)
1. `files.exclude` - 11 edges
2. `files.exclude` - 11 edges
3. `nums` - 10 edges
4. `using-agent-skills` - 10 edges
5. `test-driven-development skill` - 9 edges
6. `shipping-and-launch skill` - 9 edges
7. `planning-and-task-breakdown skill` - 8 edges
8. `spec-driven-development skill` - 8 edges
9. `security-and-hardening skill` - 8 edges
10. `idea-refine` - 8 edges

## Surprising Connections (you probably didn't know these)
- `containerized application stack` --references--> `main()`  [INFERRED]
  {{cookiecutter.project_slug}}/docker-compose.yml → my_awesome_project/src/my_awesome_project/main.py
- `Cookiecutter Cursor Template` --references--> `Cookiecutter Project Configuration`  [EXTRACTED]
  README.md → cookiecutter.json
- `Cookiecutter Hook Lifecycle` --references--> `Generated Project Customization`  [EXTRACTED]
  README.md → hooks/post_gen_project.sh
- `Configuration Management` --conceptually_related_to--> `Environment File Bootstrap`  [INFERRED]
  my_awesome_project/docs/ARCHITECTURE.md → hooks/post_gen_project.sh
- `Arrange-Act-Assert testing patterns` --conceptually_related_to--> `package metadata and entry-point tests`  [INFERRED]
  {{cookiecutter.project_slug}}/references/testing-patterns.md → my_awesome_project/tests/test_main.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Choice-driven Project Generation** — cookiecutter_project_configuration, hooks_pre_gen_project_generation_validation, hooks_post_gen_project_generated_project_customization [EXTRACTED 1.00]
- **Continuous Delivery Toolchain** — workflows_ci_continuous_integration_pipeline, workflows_ci_package_build, workflows_release_tag_driven_release [INFERRED 0.95]
- **Project Quality System** — my_awesome_project_pre_commit_config_code_quality_gate, workflows_ci_quality_checks, workflows_ci_cross_platform_tests, docs_contributing_pull_request_quality_gate [INFERRED 0.95]
- **Dependency manager rendering surfaces** — tests_test_dependency_managers_dependency_matrix, tests_test_dependency_managers_uv_consistency, cookiecutter_project_slug_readme_dependency_workflows, cookiecutter_project_slug_requirements_framework_variants, cookiecutter_project_slug_requirements_dev_development_toolchain [EXTRACTED 1.00]
- **Cross-provider CI quality pipeline** — tests_test_dependency_managers_ci_provider_matrix, cookiecutter_project_slug_gitlab_ci_quality_pipeline, circleci_config_quality_pipeline, cookiecutter_project_slug_pre_commit_config_quality_gates [EXTRACTED 1.00]
- **Cursor agent tooling stack** — scripts_sync_agent_skills_agent_skills_sync, scripts_sync_agent_skills_command_adaptation, cookiecutter_project_slug_readme_cursor_workflow, cursor_hooks_rtk_shell_rewrite, cursor_settings_ai_development_environment, cookiecutter_project_slug_prompts_prompt_audit_log [INFERRED 0.95]
- **Ship parallel specialist fan-out** — commands_ship_ship, commands_ship_parallel_fanout, agents_code_reviewer_code_reviewer, agents_security_auditor_security_auditor, agents_test_engineer_test_engineer, shipping_and_launch_skill_shipping_and_launch [EXTRACTED 1.00]
- **Build incremental TDD implementation loop** — commands_build_build, incremental_implementation_skill_incremental_implementation, test_driven_development_skill_test_driven_development, debugging_and_error_recovery_skill_debugging_and_error_recovery, planning_and_task_breakdown_skill_planning_and_task_breakdown [EXTRACTED 1.00]
- **Web performance audit tooling stack** — commands_webperf_webperf, agents_web_performance_auditor_web_performance_auditor, agents_web_performance_auditor_core_web_vitals, browser_testing_with_devtools_skill_browser_testing_with_devtools, performance_optimization_skill_performance_optimization [EXTRACTED 1.00]
- **Define-Phase Skill Chain** — interview_me_skill_interview_me, idea_refine_skill_idea_refine, spec_driven_development_skill_spec_driven_development [EXTRACTED 1.00]
- **Build and Verify Skill Cluster** — incremental_implementation_skill_incremental_implementation, source_driven_development_skill_source_driven_development, doubt_driven_development_skill_doubt_driven_development, test_driven_development_skill_test_driven_development [EXTRACTED 1.00]
- **Ship-Phase Skill Cluster** — git_workflow_and_versioning_skill_git_workflow_and_versioning, documentation_and_adrs_skill_documentation_and_adrs, observability_and_instrumentation_skill_observability_and_instrumentation, shipping_and_launch_skill_shipping_and_launch [EXTRACTED 1.00]
- **Standing quality reference checklists** — references_definition_of_done_standing_dod, references_security_checklist_security_hardening, references_observability_checklist_telemetry_checklist, references_accessibility_checklist_wcag_checklist, references_performance_checklist_web_vitals, references_testing_patterns_aaa_structure [INFERRED 0.85]
- **Agent lifecycle and orchestration model** — docs_cursor_agent_skills_lifecycle_slash_commands, references_orchestration_patterns_user_as_orchestrator, references_orchestration_patterns_sequential_lifecycle, references_orchestration_patterns_parallel_fanout, references_orchestration_patterns_anti_patterns [EXTRACTED 1.00]
- **Template app entrypoint tests and release** — cookiecutter_project_slug_main_main, cookiecutter_project_slug_init_package_metadata, tests_test_main_package_tests, workflows_release_github_release_pipeline, docs_architecture_modular_architecture [INFERRED 0.85]
- **Coverage.py sleeping-snake brand motif** — htmlcov_favicon_32_cb_c827f16f_sleeping_snake, htmlcov_favicon_32_cb_c827f16f_blue_nightcap, htmlcov_favicon_32_cb_c827f16f_coverage_pun, htmlcov_favicon_32_cb_c827f16f_coverage_py [INFERRED 0.85]

## Communities (34 total, 12 thin omitted)

### Community 0 - "Cursor Review Agents"
Cohesion: 0.07
Nodes (38): code-reviewer agent, five-axis code review framework, OWASP and LLM security review scope, security-auditor agent, Prove-It bug test pattern, test-engineer agent, Core Web Vitals audit scorecard, metric-honesty no-fabrication rule (+30 more)

### Community 1 - "Template Cursor Settings"
Cohesion: 0.07
Nodes (28): cursor.ai.autoImport, cursor.ai.codeCompletion, cursor.ai.contextWindow, cursor.ai.enabled, cursor.ai.formatOnSave, cursor.ai.inlineSuggestions, cursor.ai.lintOnSave, cursor.ai.maxTokens (+20 more)

### Community 2 - "Sample Cursor Settings"
Cohesion: 0.07
Nodes (28): cursor.ai.autoImport, cursor.ai.codeCompletion, cursor.ai.contextWindow, cursor.ai.enabled, cursor.ai.formatOnSave, cursor.ai.inlineSuggestions, cursor.ai.lintOnSave, cursor.ai.maxTokens (+20 more)

### Community 3 - "Agent Skills Workflow"
Cohesion: 0.12
Nodes (27): ci-cd-and-automation skill, /build command, /plan command, /spec command, debugging-and-error-recovery skill, Doubt Cycle (CLAIM→EXTRACT→DOUBT→RECONCILE→STOP), doubt-driven-development skill, Ideation Session Examples (+19 more)

### Community 4 - "Sample Project Docs"
Cohesion: 0.10
Nodes (27): CI/CD Pipeline Stages, Modular Scalable Architecture, Security Principles, Stateless Horizontal Scaling, Testability, Type Safety, Contribution Workflow, Pull Request Quality Gate (+19 more)

### Community 5 - "Template Docs References"
Cohesion: 0.09
Nodes (24): CI/CD lint test security build release stages, Black Ruff MyPy Pytest pre-commit toolchain, modularity type-safety testability scalability, multi-stage Docker deployment, modular scalable Python architecture, secrets scanning Bandit input validation, Sphinx documentation configuration, project contribution guidelines (+16 more)

### Community 6 - "Coverage Report Status"
Cohesion: 0.10
Nodes (23): files, z_18ee9cfd99ef5de1___init___py, z_18ee9cfd99ef5de1_main_py, format, globals, description, file, nums (+15 more)

### Community 7 - "Cookiecutter Generation"
Cohesion: 0.10
Nodes (22): CI/CD Provider Choice, Dependency Manager Choice, Optional Project Features, Cookiecutter Project Configuration, Configuration Management, CI Configuration Pruning, Dependency File Cleanup, Environment File Bootstrap (+14 more)

### Community 8 - "Template Main Tests"
Cohesion: 0.09
Nodes (17): Tests for main module., Test that version is defined., Test that the package can be imported., Test that main function executes without errors., Test that main function can be imported and called., test_import(), test_main_function_execution(), test_main_function_import() (+9 more)

### Community 9 - "Template CI Tooling"
Cohesion: 0.12
Nodes (19): CircleCI lint test security build pipeline, GitLab lint test security build pipeline, MkDocs project documentation site, pre-commit quality and security gates, AI prompt audit log, Cursor agent lifecycle workflow, Poetry uv and pip installation workflows, configurable modern Python project template (+11 more)

### Community 10 - "Cookiecutter Variables"
Cohesion: 0.11
Nodes (17): author_email, author_name, ci_cd, _copy_without_render, dependency_manager, documentation_tool, github_username, license (+9 more)

### Community 11 - "App Entrypoint Coverage"
Cohesion: 0.12
Nodes (16): containerized application stack, template package version metadata, main(), Main entry point for {{ cookiecutter.project_name }}., template application startup logging, main function coverage, 100% package coverage report, coverage generation metadata (+8 more)

### Community 12 - "Dependency Manager Tests"
Cohesion: 0.19
Nodes (13): MonkeyPatch, Path, cookiecutter_config(), isolated_environment(), Integration tests for dependency-manager template variants., Verify every supported CI provider uses the uv environment., Isolate Cookiecutter state and the post-generation git identity., Create a Cookiecutter config whose caches stay in the test directory. (+5 more)

### Community 13 - "Sample Main Tests"
Cohesion: 0.20
Nodes (9): Tests for main module., Test that version is defined., Test that the package can be imported., Test that main function executes without errors., Test that main function can be imported and called., test_import(), test_main_function_execution(), test_main_function_import() (+1 more)

### Community 14 - "Agent Orchestration"
Cohesion: 0.28
Nodes (9): Cursor agent skills routing, awesome-agentic-patterns local skill, lifecycle slash command to skill map, rtk-token-optimization local skill, orchestration anti-patterns catalog, parallel fan-out with merge pattern, user-driven sequential slash lifecycle, user as orchestrator rule (+1 more)

### Community 16 - "Coverage Favicon Brand"
Cohesion: 0.43
Nodes (8): Blue pointed nightcap, White circular badge on dark square, Sleeping-under-cover coverage pun, Coverage.py, Coverage.py 32x32 favicon, HTML coverage report favicon branding, Python, Sleeping green snake mascot

### Community 17 - "API Context Skills"
Cohesion: 0.40
Nodes (6): api-and-interface-design skill, Hyrum's Law interface principle, awesome-agentic-patterns skill, context-engineering skill, deprecation-and-migration skill, rtk-rewrite Shell preToolUse hook

### Community 18 - "Coverage Keyboard Icon"
Cohesion: 0.47
Nodes (6): Keyboard help overlay closed, HTML coverage report UI asset, Three-row key layout with spacebar, Keyboard icon (closed state), Keyboard shortcuts toggle control, Stylized computer keyboard

### Community 19 - "RTK Rewrite Hook"
Cohesion: 0.70
Nodes (3): emit_updated(), passthrough(), rtk-rewrite.sh script

### Community 20 - "Cursor Hooks Config"
Cohesion: 0.50
Nodes (3): hooks, preToolUse, version

### Community 21 - "RTK Install Script"
Cohesion: 0.83
Nodes (3): install_via_brew(), install_via_curl(), install-rtk.sh script

## Knowledge Gaps
- **155 isolated node(s):** `yaml.validate`, `project_name`, `project_slug`, `project_description`, `version` (+150 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `modular scalable Python architecture` connect `Template Docs References` to `App Entrypoint Coverage`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `Conventional Commits` connect `Template Docs References` to `Sample Project Docs`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `test-driven-development skill` (e.g. with `test-engineer agent` and `ci-cd-and-automation skill`) actually correct?**
  _`test-driven-development skill` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `yaml.validate`, `project_name`, `project_slug` to the rest of the system?**
  _195 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Cursor Review Agents` be split into smaller, more focused modules?**
  _Cohesion score 0.07254623044096728 - nodes in this community are weakly interconnected._
- **Should `Template Cursor Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.06896551724137931 - nodes in this community are weakly interconnected._
- **Should `Sample Cursor Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.06896551724137931 - nodes in this community are weakly interconnected._