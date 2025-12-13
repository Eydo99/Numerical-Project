export class FunctionParser {
  static toPythonSyntax(funcStr: string): string {
    if (!funcStr) return '';

    let result = funcStr;

    // 1. Remove spaces
    result = result.replace(/\s+/g, '');

    // 2. Normalize variables (X -> x) and symbols
    result = result.replace(/X/g, 'x');
    result = result.replace(/Y/g, 'y'); // Just in case
    result = result.replace(/Z/g, 'z'); // Just in case
    result = result.replace(/\^/g, '**');
    result = result.replace(/×/g, '*');
    result = result.replace(/÷/g, '/');

    // 3. Convert Constants & Specific Functions *BEFORE* implicit multiplication
    // (This prevents breaking things like log10 into log1*0)
    result = result.replace(/PI/gi, 'pi');
    result = result.replace(/π/g, 'pi');
    result = result.replace(/\bE\b/g, 'E');

    result = result.replace(/log10\(/g, 'log(');
    result = result.replace(/ln\(/g, 'log(');

    // 4. Handle Implicit Multiplication
    // Strategy: Insert '*' between specific token pairs

    // Case A: Number followed by [Letter, Open Paren]
    // Examples: "6x" -> "6*x", "2sin" -> "2*sin", "3(" -> "3*("
    // We assume function names start with letters.
    result = result.replace(/(\d)([a-z\(])/gi, '$1*$2');

    // Case B: Closing Paren followed by [Letter, Digit, Open Paren]
    // Examples: ")x" -> ")*x", ")2" -> ")*2", ")(" -> ")*("
    result = result.replace(/\)([\w\(])/gi, ')*$1');

    // Case C: Variable 'x' followed by [Letter, Digit, Open Paren]
    // Examples: "xx" -> "x*x", "xsin" -> "x*sin", "x2" -> "x*2", "x(" -> "x*("
    // CRITICAL: We use (?<!e) to Ignore 'x' if it is inside "exp"
    result = result.replace(/(?<!e)x([a-z\d\(])/gi, 'x*$1');

    // 5. Final Function Name Cleanups (for sympy/numpy compatibility)
    result = result.replace(/sqrt\(/g, 'sqrt(');
    result = result.replace(/cbrt\(/g, 'cbrt(');
    // Ensure exp is lowercase (just in case)
    result = result.replace(/EXP\(/gi, 'exp(');

    return result;
  }

  /**
   * Validates if the function string has balanced parentheses
   */
  static hasBalancedParentheses(funcStr: string): boolean {
    let count = 0;
    for (const char of funcStr) {
      if (char === '(') count++;
      if (char === ')') count--;
      if (count < 0) return false;
    }
    return count === 0;
  }

  /**
   * Validates basic function syntax
   */
  static isValidFunction(funcStr: string): { valid: boolean; error?: string } {
    if (!funcStr || funcStr.trim() === '') {
      return { valid: false, error: 'Function cannot be empty' };
    }

    if (!this.hasBalancedParentheses(funcStr)) {
      return { valid: false, error: 'Unbalanced parentheses' };
    }

    // Check for invalid characters (after removing valid math symbols)
    const validPattern = /^[0-9a-zA-Z+\-*/^().,\s√π×÷]+$/;
    if (!validPattern.test(funcStr)) {
      return { valid: false, error: 'Invalid characters in function' };
    }

    // Check for consecutive operators (except **)
    const consecutiveOps = /[+\-*/]{2,}/g;
    const matches = funcStr.match(consecutiveOps);
    if (matches && matches.some(m => m !== '**')) {
      return { valid: false, error: 'Consecutive operators detected' };
    }

    return { valid: true };
  }

  /**
   * Test examples to verify parser works correctly
   */
  static runTests(): void {
    const tests = [
      { input: '6x', expected: '6*x' },
      { input: '2sin(x)', expected: '2*sin(x)' },
      { input: 'xsin(x)', expected: 'x*sin(x)' },
      { input: '2(x+1)', expected: '2*(x+1)' },
      { input: '(x+1)(x-1)', expected: '(x+1)*(x-1)' },
      { input: 'xx', expected: 'x*x' },
      { input: 'x2', expected: 'x*2' }, // x multiplied by 2
      { input: 'exp(x)', expected: 'exp(x)' }, // Should NOT change to ex*p(x)
      { input: 'xexp(x)', expected: 'x*exp(x)' },
      { input: '2exp(x)', expected: '2*exp(x)' },
      { input: 'log10(x)', expected: 'log(x)' }, // Should NOT change to log1*0(x)
      { input: '3log10(x)', expected: '3*log(x)' },
      { input: 'arctan(x)', expected: 'arctan(x)' }, // Should NOT change to a*rctan
    ];

    console.log('🧪 Running Function Parser Tests...\n');

    let passed = 0;
    let failed = 0;

    tests.forEach((test, index) => {
      const result = this.toPythonSyntax(test.input);
      const success = result === test.expected;

      if (success) {
        passed++;
        console.log(`✅ Test ${index + 1}: PASSED`);
      } else {
        failed++;
        console.log(`❌ Test ${index + 1}: FAILED`);
        console.log(`   Input:    "${test.input}"`);
        console.log(`   Expected: "${test.expected}"`);
        console.log(`   Got:      "${result}"`);
      }
    });

    console.log(`\n📊 Results: ${passed} passed, ${failed} failed out of ${tests.length} tests`);
  }
}
