import { Component, Input, Output, EventEmitter  } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RootFindingService, RootFindingRequest } from '../../services/rootfinding.service';
import { FunctionParser } from '../../utils/function-parser';

interface PlotRequest {
  func: string;
  start: number;
  end: number;
}

interface SolveResult {
  solution: number | null;
  iterations: number;
  executionTime: number;
  steps: any[];
  error: string | null;
  convergenceStatus: number | null;
}

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {
  @Input() selectedMethod: string = '';
  @Output() solveComplete = new EventEmitter<SolveResult>();
  @Output() plotComplete = new EventEmitter<string>();

  clearAllSettings() {
    this.maxIterations = 100;
    this.tolerance = '0.00001';
    this.significantFigures = 5;
    this.startA = null;
    this.endB = null;
    this.initialX = null;
    this.newtonX = null;
    this.modifiedX = null;
    this.modifiedY = null;
    this.secantX0 = null;
    this.secantX1 = null;
    this.plotStart = -10;
    this.plotEnd = 10;
    this.fx = '';
    this.gx = '';
    this.caretFx = 0;
    this.caretGx = 0;
  }


  /* ----------------------------------------------------------- */
  /* ACTIVE EDIT FIELD (f(x) or g(x))                            */
  /* ----------------------------------------------------------- */
  editingTarget: 'fx' | 'gx' = 'fx';

  fx: string = '';
  gx: string = '';

  caretFx: number = 0;
  caretGx: number = 0;

  /* unified caret getter/setter */
  get caretPos(): number {
    return this.editingTarget === 'fx' ? this.caretFx : this.caretGx;
  }

  set caretPos(value: number) {
    if (this.editingTarget === 'fx') this.caretFx = value;
    else this.caretGx = value;
  }

  /* ----------------------------------------------------------- */
  /* DISPLAY (beautified output)                                 */
  /* ----------------------------------------------------------- */

  get displayFx(): string {
    return this.beautify(this.fx) || '';
  }

  get displayGx(): string {
    return this.beautify(this.gx) || '';
  }

  /* ----------------------------------------------------------- */
  /* CATEGORY + BUTTON SETS                                      */
  /* ----------------------------------------------------------- */

  activeCategory: string = 'Trig';
  categories = ['Trig','Hyp','Powers','Log','Fractions','Roots','Const'];

  numpad = [
    {label: '7', token: '7'}, {label: '8', token: '8'}, {label: '9', token: '9'}, {label: '÷', token: ' / '},
    {label: '4', token: '4'}, {label: '5', token: '5'}, {label: '6', token: '6'}, {label: '×', token: ' * '},
    {label: '1', token: '1'}, {label: '2', token: '2'}, {label: '3', token: '3'}, {label: '-', token: ' - '},
    {label: '0', token: '0'}, {label: '.', token: '.'}, {label: 'x', token: 'x'}, {label: '+', token: ' + '}
  ];

  trigButtons = [
    {label:'sin', token:'sin('}, {label:'cos', token:'cos('}, {label:'tan', token:'tan('},
    {label:'sec', token:'sec('}, {label:'csc', token:'csc('}, {label:'cot', token:'cot('},
    {label:'sin⁻¹', token:'asin('}, {label:'cos⁻¹', token:'acos('}, {label:'tan⁻¹', token:'atan('},
    {label:'sec⁻¹', token:'asec('}, {label:'csc⁻¹', token:'acsc('}, {label:'cot⁻¹', token:'acot('},
  ];

  hypButtons = [
    {label:'sinh', token:'sinh('}, {label:'cosh', token:'cosh('}, {label:'tanh', token:'tanh('},
    {label:'sech', token:'sech('}, {label:'csch', token:'csch('}, {label:'coth', token:'coth('},
    {label:'sinh⁻¹', token:'asinh('}, {label:'cosh⁻¹', token:'acosh('}, {label:'tanh⁻¹', token:'atanh('},
  ];

  powerButtons = [
    {label:'x²', token:'^2'}, {label:'x³', token:'^3'}, {label:'x^n', token:'^('},
    {label:'n^x', token:'(^)'}, {label:'n!', token:'!'}, {label:'eˣ', token:'exp('}
  ];

  logButtons = [
    {label:'ln', token:'ln('}, {label:'log', token:'log10('}, {label:'logₙ', token:'log_('}
  ];

  fractionButtons = [
    {label:'a/b', token:'( )/( )'}
  ];

  rootsButtons = [
    {label:'√', token:'sqrt('}, {label:'∛', token:'cbrt('}, {label:'ⁿ√', token:'root_('}
  ];


  constButtons = [
    {label:'π', token:'pi'}, {label:'e', token:'E'}
  ];

  /* ----------------------------------------------------------- */
  /* INSERT TOKEN                                                */
  /* ----------------------------------------------------------- */

  insert(token: string) {
    let content = this.editingTarget === 'fx' ? this.fx : this.gx;
    let caret = this.caretPos;

    const before = content.slice(0, caret);
    const after  = content.slice(caret);

    content = before + token + after;

    caret = before.length + token.length;

    if (this.editingTarget === 'fx') this.fx = content;
    else this.gx = content;

    this.caretPos = caret;
  }

  /* ----------------------------------------------------------- */
  /* CLEAR & DELETE                                              */
  /* ----------------------------------------------------------- */

  clearAll() {
    if (this.editingTarget === 'fx') this.fx = '';
    else this.gx = '';
    this.caretPos = 0;
  }

  deleteBefore() {
    let content = this.editingTarget === 'fx' ? this.fx : this.gx;

    if (this.caretPos === 0) return;

    const before = content.slice(0, this.caretPos);
    const after  = content.slice(this.caretPos);

    const newBefore = before.slice(0, -1);

    content = newBefore + after;
    this.caretPos = newBefore.length;

    if (this.editingTarget === 'fx') this.fx = content;
    else this.gx = content;
  }

  /* ----------------------------------------------------------- */
  /* CARET NAVIGATION                                            */
  /* ----------------------------------------------------------- */

  moveLeft() {
    if (this.caretPos > 0) this.caretPos--;
  }

  moveRight() {
    const length = this.editingTarget === 'fx' ? this.fx.length : this.gx.length;
    if (this.caretPos < length) this.caretPos++;
  }

  setCaretFromClick(event: MouseEvent) {
    const target = event.currentTarget as HTMLElement;
    const displaySpan = target.querySelector('.fx-value') as HTMLElement;

    if (!displaySpan) return;

    const text = this.editingTarget === 'fx' ? this.fx : this.gx;
    const displayText = this.editingTarget === 'fx' ? this.displayFx : this.displayGx;

    if (!text) {
      this.caretPos = 0;
      return;
    }

    const rect = displaySpan.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const totalWidth = rect.width;

    const clickRatio = clickX / totalWidth;
    const estimatedPos = Math.round(clickRatio * text.length);

    this.caretPos = Math.max(0, Math.min(estimatedPos, text.length));
  }







  /* ----------------------------------------------------------- */
  /* SWITCH BETWEEN f(x) AND g(x)                                */
  /* ----------------------------------------------------------- */

  toggleEditing() {
    this.editingTarget = this.editingTarget === 'fx' ? 'gx' : 'fx';
    this.caretPos = 0; // reset caret when switching field
  }

  /* ----------------------------------------------------------- */
  /* BEAUTIFIER (for DISPLAY ONLY)                               */
  /* ----------------------------------------------------------- */

  beautify(raw: string): string {
    if (!raw) return '';
    let s = raw;
    s = s.replace(/\^2/g, '²').replace(/\^3/g, '³');
    s = s.replace(/\*/g, ' × ').replace(/\//g, ' ÷ ');
    s = s.replace(/pi/gi, 'π');
    s = s.replace(/\bE\b/g, 'e');
    s = s.replace(/exp\(/g, 'e^(');
    return s.trim();
  }

  /* ----------------------------------------------------------- */
  /* GENERAL SETTINGS + METHOD PARAMS                             */
  /* ----------------------------------------------------------- */

  maxIterations: number = 50;
  tolerance: string = '0.00001';
  significantFigures: number = 6;

  startA: number | null = null;
  endB: number | null = null;

  initialX: number | null = null;
  newtonX: number | null = null;
  modifiedX: number | null = null;
  modifiedY: number | null = null;

  secantX0: number | null = null;
  secantX1: number | null = null;
  plotStart: number = -10;
  plotEnd: number = 10;
  isPlotting: boolean = false;


  //Plotting

  constructor(private rootFindingService: RootFindingService) {}

  plotFunction() {
    if (!this.fx) {
      alert('Please enter a function first!');
      return;
    }

    const validation = FunctionParser.isValidFunction(this.fx);
    if (!validation.valid) {
      alert(`Invalid function: ${validation.error}`);
      return;
    }

    this.isPlotting = true;
    const parsedFunc = FunctionParser.toPythonSyntax(this.fx);
    console.log('Plotting function:', parsedFunc);

    this.rootFindingService.plot(parsedFunc, this.plotStart, this.plotEnd).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        this.plotComplete.emit(url);
        this.isPlotting = false;
      },
      error: (err) => {
        console.error('Plotting error:', err);
        alert('Error plotting function. Check your function syntax.');
        this.isPlotting = false;
      }
    });
  }




  /* ----------------------------------------------------------- */
  /* RUN METHOD CALL                                             */
  /* ----------------------------------------------------------- */

  runMethod() {
    if (!this.fx) {
      alert('Please enter a function f(x)!');
      return;
    }

    if (!this.selectedMethod) {
      alert('Please select a method from the top bar!');
      return;
    }
    const validation = FunctionParser.isValidFunction(this.fx);
    if (!validation.valid) {
      alert(`Invalid function: ${validation.error}`);
      return;
    }

    const parsedFunc = FunctionParser.toPythonSyntax(this.fx);
    console.log('Original function:', this.fx);
    console.log('Parsed function:', parsedFunc);

    // Build the payload based on the selected method
    const payload: RootFindingRequest = {
      func: parsedFunc,
      tol: parseFloat(this.tolerance),
      max_itrs: this.maxIterations,
      sig_figs: this.significantFigures,
      single_step: true
    };

    // Add method-specific parameters
    switch (this.selectedMethod) {
      case 'bisection':
      case 'false-position':
        if (this.startA === null || this.endB === null) {
          alert('Please enter both interval boundaries (a and b)!');
          return;
        }
        payload.first = this.startA;
        payload.second = this.endB;
        break;

      case 'fixed-point':
        if (this.initialX === null) {
          alert('Please enter initial guess x₀!');
          return;
        }
        if (!this.gx) {
          alert('Please enter g(x) function!');
          return;
        }
        const gxValidation = FunctionParser.isValidFunction(this.gx);
        if (!gxValidation.valid) {
          alert(`Invalid g(x) function: ${gxValidation.error}`);
          return;
        }


        payload.first = this.initialX;
        const parsedGx = FunctionParser.toPythonSyntax(this.gx);
        console.log('Original g(x):', this.gx);
        console.log('Parsed g(x):', parsedGx);
        payload.func = parsedGx; ////////////////////////////////////
        break;

      case 'newton-orig':
        if (this.newtonX === null) {
          alert('Please enter initial guess x₀!');
          return;
        }
        payload.first = this.newtonX;
        break;

      case 'newton-mod':
        if (this.modifiedX === null) {
          alert('Please enter initial guess X!');
          return;
        }
        payload.first = this.modifiedX;
        // If modifiedY is provided, use it as multiplicity, otherwise send null for Modified 2
        payload.multiplicity = this.modifiedY !== null ? this.modifiedY : null;
        break;

      case 'secant':
        if (this.secantX0 === null || this.secantX1 === null) {
          alert('Please enter both initial guesses (x₀ and x₁)!');
          return;
        }
        payload.first = this.secantX0;
        payload.second = this.secantX1;
        break;
    }
    console.log('Sending payload:', payload);

    // Call the service
    this.rootFindingService.solve(this.selectedMethod, payload).subscribe({
      next: (response) => {
        console.log('Backend response:', response);

        // Check if response has sol property - if not, it's likely an error
        if (response.sol === undefined || response.sol === null) {
          // Try to extract error message from response
          let errorMsg = 'Method failed to find a solution';

          if (response.error) {
            errorMsg = response.error;
          } else if (response.problem) {
            errorMsg = response.problem;
          }

          const result: SolveResult = {
            solution: null,
            iterations: response.itrs || 0,
            executionTime: response.exec_time || 0,
            steps: response.steps || [],
            error: errorMsg,
            convergenceStatus: response.status !== undefined ? response.status : null
          };
          this.solveComplete.emit(result);
          return;
        }

        // Success case
        const result: SolveResult = {
          solution: response.sol,
          iterations: response.itrs || 0,
          executionTime: response.exec_time || 0,
          steps: response.steps || [],
          error: null,
          convergenceStatus: response.status !== undefined ? response.status : null
        };
        this.solveComplete.emit(result);
      },
      error: (err) => {
        console.error('HTTP Error from backend:', err);

        // Extract error message from different possible locations
        let errorMessage = 'An error occurred while solving';

        if (err.error) {
          try {
            // If error is already an object with error field
            if (typeof err.error === 'object' && err.error.error) {
              errorMessage = err.error.error;
            }
            // If error is a JSON string
            else if (typeof err.error === 'string') {
              try {
                const parsed = JSON.parse(err.error);
                errorMessage = parsed.error || err.error;
              } catch {
                errorMessage = err.error;
              }
            }
          } catch {
            errorMessage = 'Failed to parse error response';
          }
        } else if (err.message) {
          errorMessage = err.message;
        }

        // Clean up error message
        if (errorMessage.includes('Error:')) {
          errorMessage = errorMessage.replace('Error:', '').trim();
        }

        const result: SolveResult = {
          solution: null,
          iterations: 0,
          executionTime: 0,
          steps: [],
          error: errorMessage,
          convergenceStatus: null
        };
        this.solveComplete.emit(result);
      }
    });
  }
}
