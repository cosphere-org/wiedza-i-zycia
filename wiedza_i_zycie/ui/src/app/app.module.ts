import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { EditionsCardComponent } from './editions-grid/editions-card/editions-card.component';
import { NavigationComponent } from './@shared/navigation/navigation.component';
import { FlexLayoutModule } from '@angular/flex-layout/';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { HttpClientModule } from '@angular/common/http';
import { MainViewComponent } from './main-view/main-view.component';
import { RouterModule } from '@angular/router';
import { RightNavComponent } from './@shared/right-nav/right-nav.component';

// import { SharedDependenciesModule} from './shared-dependencies/shared-dependencies.module'

@NgModule({
  declarations: [
    AppComponent,
    EditionsCardComponent,
    NavigationComponent,
    ToolbarComponent,
    MainViewComponent,
    RightNavComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    FlexLayoutModule,
    FormsModule,
    HttpClientModule,
    // SharedDependenciesModule,
    RouterModule.forRoot([
      { path: '', component: MainViewComponent },
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
