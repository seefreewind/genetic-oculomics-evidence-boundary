#!/usr/bin/env Rscript
## Restricted MR-PRESSO sensitivity pass for Phase 2A. No causal taxonomy.
suppressPackageStartupMessages(library(MRPRESSO))
args <- commandArgs(trailingOnly=TRUE)
if (length(args) < 2) stop("usage: run_phase2a_mrpresso.R harmonized.tsv output.tsv")
input <- read.delim(args[1], stringsAsFactors=FALSE, check.names=FALSE)
outfile <- args[2]
groups <- split(input, list(input$pair_key, input$direction), drop=TRUE)
rows <- list(); k <- 0L
for (nm in names(groups)) {
  d <- groups[[nm]]
  pair <- as.character(d$pair_key[1]); direction <- as.character(d$direction[1])
  if (nrow(d) < 4) {
    k <- k + 1L; rows[[k]] <- data.frame(pair_key=pair, direction=direction, status="NOT_ELIGIBLE_LT4_IV", global_p=NA, outlier_count=NA, stringsAsFactors=FALSE); next
  }
  ans <- tryCatch(
    mr_presso(BetaOutcome="beta_out", BetaExposure="beta_exp", SdOutcome="se_out", SdExposure="se_exp",
              data=d, OUTLIERtest=TRUE, DISTORTIONtest=TRUE, SignifThreshold=0.05,
              NbDistribution=1000, seed=20260918),
    error=function(e) e
  )
  status <- "FAILED"; gp <- NA_real_; oc <- NA_integer_
  if (!inherits(ans, "error")) {
    status <- "COMPUTED_NO_OUTLIER"
    if (!is.null(ans$`Global Test`$Pvalue)) gp <- as.numeric(ans$`Global Test`$Pvalue)
    if (!is.null(ans$`Outlier Test`$`Outlier Indices`)) {
      oi <- ans$`Outlier Test`$`Outlier Indices`; oc <- if (is.null(oi)) 0L else length(oi)
      if (!is.na(oc) && oc > 0) status <- "COMPUTED_OUTLIERS_FLAGGED"
    }
  }
  k <- k + 1L; rows[[k]] <- data.frame(pair_key=pair, direction=direction, status=status, global_p=gp, outlier_count=oc, stringsAsFactors=FALSE)
}
out <- if (length(rows)) do.call(rbind, rows) else data.frame(pair_key=character(), direction=character(), status=character(), global_p=numeric(), outlier_count=integer())
dir.create(dirname(outfile), recursive=TRUE, showWarnings=FALSE)
write.table(out, outfile, sep="\t", quote=FALSE, row.names=FALSE, na="NA")
cat(sprintf("mr_presso_groups=%d output=%s\n", nrow(out), outfile))
