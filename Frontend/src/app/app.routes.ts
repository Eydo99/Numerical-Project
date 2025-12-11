import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { Phase1Component } from './phase1/phase1.component';
import { Phase2Component } from './phase2/phase2.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'phase1', component: Phase1Component },
  { path: 'phase2', component: Phase2Component }
];
