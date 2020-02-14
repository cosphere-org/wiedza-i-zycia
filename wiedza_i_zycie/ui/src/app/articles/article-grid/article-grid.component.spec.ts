import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleGridComponent } from './article-grid.component';

describe('ArticleGridComponent', () => {
  let component: ArticleGridComponent;
  let fixture: ComponentFixture<ArticleGridComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleGridComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleGridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
