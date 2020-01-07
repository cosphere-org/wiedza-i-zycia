import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditionsGridComponent } from './editions-grid.component';

describe('EditionsGridComponent', () => {
  let component: EditionsGridComponent;
  let fixture: ComponentFixture<EditionsGridComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditionsGridComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditionsGridComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
