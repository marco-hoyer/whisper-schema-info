__author__ = 'mhoyer'

import sys
import logging

import argparse


class SchemaInfo:

    def __init__(self, args):
        # Injecting the Carbon Lib Path if needed
        if args.carbonlibdir is not None:
            sys.path.insert(0, args.carbonlibdir)

        try:
            from carbon import conf
            from carbon.conf import settings
            # set carbon config dir
            settings.CONF_DIR = args.carbonconfigdir
            from carbon.storage import loadStorageSchemas, loadAggregationSchemas, DefaultSchema, PatternSchema
        except ImportError as e:
            raise SystemExit('[ERROR] Can\'t find the carbon module, try using --carbonlibdir to explicitly include the path')

        self.DefaultSchema = DefaultSchema
        self.PatternSchema = PatternSchema

        # load schemas from storage-schemas.conf and storage-aggregation.conf using carbon module
        self.storage_schemas = loadStorageSchemas()
        self.aggregation_schemas = loadAggregationSchemas()

    def _init_logger(self):
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)

    def set_log_level(self, verbose):
            if verbose:
                    level=logging.DEBUG
            else:
                    level=logging.INFO
            logging.getLogger().setLevel(level)


    def get_storage_config_for_metric_string(self, metric):
        # find schema for given metric name
        storage_schema = self.get_schema_for_metric(self.storage_schemas, metric)
        return [archive.getTuple() for archive in storage_schema.archives]

    def get_aggregation_config_for_metric_string(self, metric):
        # find schema for given metric name
        aggregation_schema = self.get_schema_for_metric(self.aggregation_schemas, metric)
        return aggregation_schema.archives

    def get_schema_info(self, schema):
        if isinstance(schema, self.PatternSchema):
            return str(schema.pattern)
        elif isinstance(schema, self.DefaultSchema):
                return str("DefaultSchema with %s") % schema.archives[0]
        else:
            return "Unknown schema type: " + type(schema)

    def get_schema_for_metric(self, schemas, metric):
        for schema in schemas:
            self.logger.debug("Looking at pattern: " + self.get_schema_info(schema))
            # use matching method directly from carbon to ensure equal results
            if schema.matches(metric):
                self.logger.info("(Using first matching pattern: " + self.get_schema_info(schema) + ")")
                return schema
        return None

    def print_storage_config(self, metric):
        storage_config = self.get_storage_config_for_metric_string(metric)
        archive_id = 0
        for element in storage_config:
            self.logger.info("Archive %i: Seconds per point: %i, Datapoints to save: %i" % (archive_id, element[0], element[1]))
            archive_id = archive_id + 1

    def print_aggregation_config(self, metric):
        aggregation_config = self.get_aggregation_config_for_metric_string(metric)
        self.logger.info("xFilesFactor: " + str(aggregation_config[0]))
        self.logger.info("Aggregation method: " + str(aggregation_config[1]))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('metricname', help="Dot-separated metric name", type=str)
    parser.add_argument('--carbonconfigdir', help="Path to carbon config dir containing storage-aggregation.conf and storage-schemas.conf", type=str, default= "/etc/carbon/")
    parser.add_argument('--carbonlibdir', help="Path to carbon libraries", type=str, default="/opt/graphite/lib/")
    parser.add_argument('--verbose', help="Verbose output", action="store_true", default = False)
    return parser.parse_args()

def main():
    args = parse_arguments()
    schema = SchemaInfo(args)
    schema._init_logger()
    schema.set_log_level(args.verbose)
    schema.logger.info("STORAGE CONFIG:")
    schema.print_storage_config(args.metricname)
    schema.logger.info("")
    schema.logger.info("AGGREGATION CONFIG:")
    schema.print_aggregation_config(args.metricname)

if __name__ == '__main__':
    main()