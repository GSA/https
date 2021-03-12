'use strict';

const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const exec = require('child_process').exec;

const PORT = process.env.PORT || '8000';

const USWDS_DIST = 'node_modules/uswds/dist';
const USWDS_DIST_DIR = path.join(__dirname, ...USWDS_DIST.split('/'));

const PROJECT_SASS_SRC = "./assets/sass/**/*.scss";
const PROJECT_CSS_DEST = './assets/css'

const PROJECT_ASSETS_SRC = `${USWDS_DIST}/@(js|fonts|img)/**/**`
const PROJECT_ASSETS_DEST = './assets/vendor/uswds'


gulp.task('copy-uswds-assets', () => {
  return gulp.src(PROJECT_ASSETS_SRC)
    .pipe(gulp.dest(PROJECT_ASSETS_DEST));
});

gulp.task('build-sass', () => {
  return gulp.src(PROJECT_SASS_SRC)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        path.join(USWDS_DIST_DIR, 'scss'),
      ]
    }).on('error', sass.logError))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(PROJECT_CSS_DEST));
});

/** entry points **/

// gulp.task('init', gulp.series('copy-uswds-assets'));

gulp.task('watch', () => {
  gulp.watch(PROJECT_SASS_SRC, gulp.series('copy-uswds-assets','build-sass'));
});

gulp.task('default', gulp.series('copy-uswds-assets', 'build-sass'));
