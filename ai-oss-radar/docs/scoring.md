# Scoring Model

AI OSS Radar scores repositories on a 0-100 scale across three dimensions.

## Usage

Usage estimates how widely a repository is being adopted.

Signals:

- Stars
- Forks
- Watchers

The implementation uses logarithmic normalization so very large repositories do not completely flatten smaller but meaningful projects.

## Ecosystem Importance

Ecosystem importance estimates whether a repository has reuse and integration signals beyond raw popularity.

Signals:

- Star reach
- Fork-to-star ratio
- Topic metadata
- License presence
- Main language presence
- Organization ownership

Missing license or topic metadata lowers confidence because it makes reuse and discovery harder.

## Activity

Activity estimates recent maintenance health.

Signals:

- Recent push date
- Recent update date
- Archived or disabled status
- Open issue pressure relative to project size
- Fork penalty

Archived and disabled repositories are penalized even if they have strong historical adoption.

## Overall Score

The overall score is a weighted blend:

- Usage: 35%
- Ecosystem importance: 35%
- Activity: 30%

These weights favor projects that are both important and alive. For dependency selection, treat the score as a shortlist generator and still review code quality, security posture, license compatibility, and governance.
