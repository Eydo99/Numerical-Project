import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './input.component.html',
  styleUrls: ['./input.component.css']
})
export class InputComponent {
  @Input() selectedMethod: string = '';

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
  categories = ['Trig','Hyp','Powers','Log','Fractions','Roots','Var','Const'];

  numpad = [
    {label: '7', token: '7'}, {label: '8', token: '8'}, {label: '9', token: '9'}, {label: '÷', token: ' / '},
    {label: '4', token: '4'}, {label: '5', token: '5'}, {label: '6', token: '6'}, {label: '×', token: ' * '},
    {label: '1', token: '1'}, {label: '2', token: '2'}, {label: '3', token: '3'}, {label: '-', token: ' - '},
    {label: '0', token: '0'}, {label: '.', token: '.'}, {label: '=', token: '='}, {label: '+', token: ' + '}
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

  varButtons = [
    {label:'X', token:'X'}, {label:'Y', token:'Y'}, {label:'Z', token:'Z'}
  ];

  constButtons = [
    {label:'π', token:'PI'}, {label:'e', token:'E'}
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
    s = s.replace(/PI/g, 'π').replace(/\bE\b/g, 'e');
    s = s.replace(/exp\(/g, 'e^(');
    return s.trim();
  }

  /* ----------------------------------------------------------- */
  /* GENERAL SETTINGS + METHOD PARAMS                             */
  /* ----------------------------------------------------------- */

  maxIterations: number = 100;
  tolerance: string = '0.0001';
  significantFigures: number = 5;

  startA: number | null = null;
  endB: number | null = null;

  initialX: number | null = null;
  newtonX: number | null = null;
  modifiedX: number | null = null;
  modifiedY: number | null = null;

  secantX0: number | null = null;
  secantX1: number | null = null;

  /* ----------------------------------------------------------- */
  /* RUN METHOD CALL                                             */
  /* ----------------------------------------------------------- */

  runMethod() {
    const payload = {
      fx: this.fx,
      gx: this.gx,
      settings: {
        maxIterations: this.maxIterations,
        tolerance: this.tolerance,
        significantFigures: this.significantFigures
      },
      method: this.selectedMethod,
      params: {
        a: this.startA,
        b: this.endB,
        x0: this.initialX,
        newtonX: this.newtonX,
        modX: this.modifiedX,
        modY: this.modifiedY,
        secantX0: this.secantX0,
        secantX1: this.secantX1
      }
    };

    console.log('RUN METHOD payload:', payload);
    alert('Run method triggered — check console.');
  }
}
