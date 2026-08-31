#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: "Verify the Blueprint tables (Physics, Chemistry, Mathematics) in the app against the official KSEAB 2026-27 II PUC blueprint PDFs and fix any mismatch."

frontend:
  - task: "Blueprint tables match official KSEAB PDFs (Physics/Chemistry/Mathematics)"
    implemented: true
    working: true
    file: "frontend/src/lib/blueprints.js, frontend/src/pages/Blueprint.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
        -working: "NA"
        -agent: "main"
        -comment: "Verified Physics & Chemistry blueprint data already matched the official PDFs exactly. Found and fixed the Mathematics blueprint: Part E was a single 6-mark column with wrong chapter mapping. Split into two columns — Part E (6 marks: Integrals CH7 + Linear Programming CH12) and Part E (4 marks: Determinants CH4 + Continuity CH5). Also corrected Matrices (D=1), Differential Equations (C blank, D=1), Linear Programming (C blank). Column totals now: A 20/20, B 06/09 12/18, C 06/09 18/27, D 04/07 20/35, E6 01/02 06/12, E4 01/02 04/08. Needs verification that all three blueprint tables render and match the official values."
        -working: true
        -agent: "testing"
        -comment: "✅ VERIFIED ALL THREE BLUEPRINTS SUCCESSFULLY. MATHEMATICS: Confirmed 6 part columns (PART-A 1M, PART-B 2M, PART-C 3M, PART-D 5M, PART-E 6M, PART-E 4M). All critical chapter mappings verified: Determinants Ch4 E4=1, Continuity Ch5 E4=1, Integrals Ch7 E6=1, Linear Programming Ch12 E6=1 C=blank, Matrices Ch3 D=1, Differential Equations Ch9 C=blank D=1. Bottom totals: Questions 20/20, 06/09, 06/09, 04/07, 01/02, 01/02; Marks 20/20, 12/18, 18/27, 20/35, 06/12, 04/08. PHYSICS: Subject 33, Max 70, 4 parts A/B/C/D, 14 chapters, totals Q: 20/20, 05/08, 05/08, 05/09; M: 20/20, 10/16, 15/24, 25/45. CHEMISTRY: Subject 34, Max 70, 4 parts A/B/C/D, 10 units, totals Q: 20/20, 03/05, 08/15, 04/06; M: 20/20, 06/10, 24/45, 20/30. All tables render correctly with official KSEAB 2026-27 values. Screenshots captured for evidence."

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 0
  run_ui: false

test_plan:
  current_focus: []
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
    -agent: "main"
    -message: "Please verify the Blueprint page for all three subjects. Navigate to /subject/physics/blueprint, /subject/chemistry/blueprint, /subject/math/blueprint. Confirm the tables render with correct per-chapter part counts and totals. CRITICAL FOCUS = Mathematics: it must now show SIX part columns (PART-A 1mark, PART-B 2mark, PART-C 3mark, PART-D 5mark, PART-E 6mark, PART-E 4mark). Determinants row -> 4-mark E = 1; Continuity and Differentiability -> 4-mark E = 1; Integrals -> 6-mark E = 1; Linear Programming -> 6-mark E = 1. Bottom totals row for marks should read 20/20, 12/18, 18/27, 20/35, 06/12, 04/08. Physics (Max 70, parts A/B/C/D, totals 20/20, 10/16, 15/24, 25/45) and Chemistry (Max 70, parts A/B/C/D, totals 20/20, 06/10, 24/45, 20/30) should also render correctly."
    -agent: "testing"
    -message: "✅ VERIFICATION COMPLETE - ALL BLUEPRINTS PASS. Tested all three blueprint pages (/subject/math/blueprint, /subject/physics/blueprint, /subject/chemistry/blueprint). Mathematics blueprint fix is working perfectly: the two Part-E columns (6 Mark and 4 Mark) are rendering correctly with accurate chapter mappings. All critical cells verified against official KSEAB 2026-27 values. Physics and Chemistry blueprints also render correctly. Screenshots captured. No issues found. Ready for user acceptance."
