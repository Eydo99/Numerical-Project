export class FunctionParser {
  static toPythonSyntax(funcStr: string): string {
    if (!funcStr) return '';

    let result = funcStr;

    // removing spaces
    result = result.replace(/\s+/g, '');

    // 2. Convert uppercase X to lowercase x (Python variable)
    result = result.replace(/X/g, 'x');
    result = result.replace(/Y/g, 'y');
    result = result.replace(/Z/g, 'z');

    // ^ to **
    result = result.replace(/\^/g, '**');

    // × to *
    result = result.replace(/×/g, '*');

    // ÷ to /
    result = result.replace(/÷/g, '/');

    // Convert constants
    result = result.replace(/PI/gi, 'pi');
    result = result.replace(/π/g, 'pi');
    result = result.replace(/\bE\b/g, 'E');  // Euler's number

    // Handle implicit multiplication (e.g., 2x -> 2*x, xsin -> x*sin)
    // Number followed by variable or function
    result = result.replace(/(\d)([y-z])/gi, '$1*$2');
    // Variable followed by function
    result = result.replace(/([a-z])([y-z]+\()/gi, '$1*$2');
    // Closing paren followed by number or variable
    result = result.replace(/\)(\d|[y-z])/gi, ')*$1');
    // Variable/number followed by opening paren
    result = result.replace(/([y-z\d])\(/gi, '$1*(');

    // Convert trigonometric functions to sympy/numpy format
    const trig_functions = [
      'sin', 'cos', 'tan', 'sec', 'csc', 'cot',
      'asin', 'acos', 'atan', 'asec', 'acsc', 'acot',
      'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth',
      'asinh', 'acosh', 'atanh'
    ];

    // Convert log functions
    result = result.replace(/log10\(/g, 'log(');
    result = result.replace(/ln\(/g, 'log(');

    // Convert sqrt and root functions
    result = result.replace(/sqrt\(/g, 'sqrt(');
    result = result.replace(/cbrt\(/g, 'cbrt(');

    //  Handle exp function
    result = result.replace(/exp\(/g, 'exp(');


    result = result.replace(/\*\*/g, '**');
    result = result.replace(/\*\*\*/g, '**');

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
      { input: '2 * x + 3', expected: '2*x+3' },
      { input: 'X ^ 2 + 3 * X', expected: 'x**2+3*x' },
      { input: 'sin ( x )', expected: 'sin(x)' },
      { input: 'x × 5 ÷ 2', expected: 'x*5/2' },
      { input: '2x + 3', expected: '2*x+3' },
      { input: 'xsin(x)', expected: 'x*sin(x)' },
      { input: 'exp ( x ) + π', expected: 'exp(x)+pi' },
      { input: 'ln ( x ) + log10 ( x )', expected: 'log(x)+log(x)' },
      { input: '3x^2 + 2x + 1', expected: '3*x**2+2*x+1' },
      { input: 'sqrt ( x )', expected: 'sqrt(x)' },
      { input: '(x + 1)(x - 1)', expected: '(x+1)*(x-1)' },
      { input: 'E ^ x', expected: 'E**x' },
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
